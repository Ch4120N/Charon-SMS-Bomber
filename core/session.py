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


def load_session() -> Optional[dict[str, Any]]:
    if not SESSION_PATH.exists():
        return None
    try:
        data = json.loads(SESSION_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not data.get("targets"):
        return None
    data["threads"] = int(data.get("threads", 10))
    data["rounds"] = int(data.get("rounds", 10))
    data["delay"] = float(data.get("delay", 0.05))
    return data


__all__ = ["save_session", "load_session"]