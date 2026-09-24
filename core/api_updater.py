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
        local_count=local_count,
        remote_count=remote_count,
        local_hash=local_hash,
        remote_hash=remote_hash,
        remote_version=str(manifest.get("version", "unknown")),
        manifest=manifest,
    )


def download_apis(
    apis_url: str = DEFAULT_APIS_URL,
    timeout: int = 30,
    progress_cb: Optional[Callable[[int, int], None]] = None,
) -> Path:
    """
    Stream-download the remote apis.json. Calls progress_cb(chunk, total)
    as data arrives. Backs up the existing apis.json before overwriting.
    Returns the path to the newly-installed file.
    """
    # Backup existing
    if APIS_PATH.exists():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = APIS_PATH.with_name(f"apis.json.bak.{ts}")
        shutil.copy2(APIS_PATH, backup)

    tmp = APIS_PATH.with_suffix(".json.tmp")
    with requests.get(apis_url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length") or 0)
        written = 0
        with tmp.open("wb") as fh:
            for chunk in r.iter_content(chunk_size=8192):
                if not chunk:
                    continue
                fh.write(chunk)
                written += len(chunk)
