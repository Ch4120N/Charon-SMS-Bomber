"""Remote API registry updater — checks GitHub for a newer apis.json."""
from __future__ import annotations

import hashlib
import json
import shutil
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

import requests

from utils.paths import APIS_PATH, BASE_DIR


# ──────────────────────────────────────────────────────────────────────
#  Where to pull the manifest + latest apis.json from.
#  Adjust these to your release URLs.
# ──────────────────────────────────────────────────────────────────────
DEFAULT_MANIFEST_URL = (
    "https://raw.githubusercontent.com/Ch4120N/Charon-SMS-Bomber/"
    "master/manifest.json"
)
DEFAULT_APIS_URL = (
    "https://raw.githubusercontent.com/Ch4120N/Charon-SMS-Bomber/"
    "master/apis.json"
)


@dataclass
class UpdateCheck:
    available: bool
    local_count: int
    remote_count: int
    local_hash: str
    remote_hash: str
    remote_version: str
    manifest: dict[str, Any]


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha256_file(p: Path) -> str:
    return _sha256_bytes(p.read_bytes())


def _count_apis(path: Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return len(data) if isinstance(data, list) else len(data.get("apis", []))
    except Exception:
        return 0


def check_for_updates(
    manifest_url: str = DEFAULT_MANIFEST_URL,
    apis_url: str = DEFAULT_APIS_URL,
    timeout: int = 10,
) -> UpdateCheck:
    """Fetch remote manifest + apis.json, compare with local."""
    local_hash = _sha256_file(APIS_PATH) if APIS_PATH.exists() else ""
    local_count = _count_apis(APIS_PATH) if APIS_PATH.exists() else 0

    # Remote manifest
    try:
        mr = requests.get(manifest_url, timeout=timeout)
        mr.raise_for_status()
        manifest = mr.json()
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch manifest: {exc}") from exc

    # Remote apis.json
    try:
        ar = requests.get(apis_url, timeout=timeout)
        ar.raise_for_status()
        remote_bytes = ar.content
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch apis.json: {exc}") from exc

    remote_hash = _sha256_bytes(remote_bytes)
    try:
        remote_data = json.loads(remote_bytes)
        remote_count = (
            len(remote_data) if isinstance(remote_data, list)
            else len(remote_data.get("apis", []))
        )
    except Exception:
        remote_count = 0

    available = remote_hash != local_hash
    return UpdateCheck(
        available=available,
