"""Session persistence (continue.json)."""
from __future__ import annotations

import json
from typing import Any, Optional

from utils.paths import SESSION_PATH


def save_session(
    targets: list[str], threads: int, rounds: int, delay: float
) -> None:
    SESSION_PATH.write_text(
        json.dumps(
            {"targets": targets, "threads": threads, "rounds": rounds, "delay": delay},
            indent=4,
        ),
        encoding="utf-8",
    )
