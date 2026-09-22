"""HTTP sender with retries, proxies, and response-body verification."""
from __future__ import annotations

import json
import random
import re
import time
from typing import Any, Optional

import requests
from fake_useragent import UserAgent


#  Response body analysis
_NEGATIVE_KEYS = {"error", "errors", "err", "exception", "fault"}
_POSITIVE_STRINGS = {"ok", "success", "true", "sent", "done", "accepted"}
_NEGATIVE_STRINGS = {"error", "failed", "fail", "false", "invalid", "denied", "rejected"}


def _walk(obj: Any, depth: int = 0) -> Optional[bool]:
    """Return True/False if body clearly says success/failure; None if unknown."""
    if depth > 3:
        return None

    if isinstance(obj, dict):
        # error-bearing keys → failure
        for k in _NEGATIVE_KEYS:
            if k in obj:
                v = obj[k]
                if v not in (None, "", [], {}, 0, "0"):
                    return False

        # positive booleans
        for k in ("success", "ok", "valid", "sent", "result"):
            v = obj.get(k)
            if isinstance(v, bool):
                return v
            if isinstance(v, str):
                low = v.lower()
                if low in _POSITIVE_STRINGS:
                    return True
                if low in _NEGATIVE_STRINGS:
                    return False

        # numeric codes — 0 / 200 / 201 = ok, >= 400 = bad
        for k in ("code", "status_code", "statusCode", "status"):
            v = obj.get(k)
            if isinstance(v, int):
                if v in (0, 200, 201, 202, 204):
                    return True
                if v >= 400:
                    return False
            if isinstance(v, str) and v.isdigit():
                n = int(v)
                if n in (0, 200, 201, 202, 204):
                    return True
                if n >= 400:
                    return False

        # status string
        v = obj.get("status")
        if isinstance(v, str):
            low = v.lower()
            if low in _POSITIVE_STRINGS:
                return True
            if low in _NEGATIVE_STRINGS:
                return False

        # descend
        for k in ("data", "result", "response", "body", "payload"):
            if k in obj:
                verdict = _walk(obj[k], depth + 1)
                if verdict is not None:
                    return verdict

    elif isinstance(obj, list) and obj:
        # heuristic — any non-empty list of errors = failure
        return None

    return None


def inspect_response_body(content: bytes) -> Optional[bool]:
    """Best-effort body verdict. None = can't determine."""
    if not content:
        return None
    try:
        data = json.loads(content)
    except Exception:
        # plaintext fallback
        text = content[:512].decode("utf-8", errors="ignore").lower()
        if any(w in text for w in ("error", "invalid", "failed", "denied")):
            return False
        if any(w in text for w in ("success", "sent", "ok")):
            return True
        return None

