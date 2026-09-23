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

