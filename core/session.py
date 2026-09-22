"""Session persistence (continue.json)."""
from __future__ import annotations

import json
from typing import Any, Optional

from utils.paths import SESSION_PATH


def save_session(
    targets: list[str], threads: int, rounds: int, delay: float
) -> None:
