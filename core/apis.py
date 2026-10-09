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
