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

