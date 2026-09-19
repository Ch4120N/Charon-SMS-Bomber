"""API registry: load, filter, dedupe, expand."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from utils.paths import APIS_PATH

# Applied to every request unless the API overrides them.
DEFAULT_HEADERS: dict[str, str] = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Connection": "keep-alive",
}


def load_apis(path: Path | None = None) -> list[dict[str, Any]]:
    p = path or APIS_PATH
    if not p.exists():
        raise FileNotFoundError(f"API registry not found: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError(f"{p.name} must contain a non-empty JSON list.")
    # Normalize: ensure every entry has sane fields.
    out: list[dict[str, Any]] = []
    for entry in data:
        if not isinstance(entry, dict) or "url" not in entry:
            continue
        e = dict(entry)
        e.setdefault("name", e["url"])
        e.setdefault("method", "POST")
        e.setdefault("enabled", True)
        e.setdefault("tags", [])
        e.setdefault("weight", 1)
        e.setdefault("headers", {})
        out.append(e)
    return out


def api_key(api: dict[str, Any]) -> str:
    return f"{api.get('method', 'POST').upper()} {api.get('url', '?')}"


def filter_apis(
    apis: list[dict[str, Any]],
    tags: list[str] | None = None,
    enabled_only: bool = True,
) -> list[dict[str, Any]]:
    out = []
    tagset = {t.lower() for t in (tags or [])}
    for api in apis:
        if enabled_only and not api.get("enabled", True):
            continue
        if tagset:
            api_tags = {t.lower() for t in api.get("tags", [])}
            if not (api_tags & tagset):
                continue
        out.append(api)
    return out


def expand_api(api: dict[str, Any], phone: str) -> dict[str, Any]:
    """
    Substitute placeholders inside any string of the API definition.

    Tokens:
      {cc}    → 9123456789        (no plus, no leading zero)
      {intl}  → +989123456789     (E.164)
      {local} → 09123456789       (leading zero)
      {ts}    → unix ms timestamp
    """
    cc = phone.replace("+98", "")
    intl = phone
    local = "0" + cc
    ts = str(int(time.time() * 1000))

