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
