"""Persist a small history of attack sessions."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from utils.paths import BASE_DIR


HISTORY_PATH = BASE_DIR / "history.json"
MAX_ENTRIES = 50


@dataclass
class HistoryEntry:
    ts: str
