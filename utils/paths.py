from __future__ import annotations

from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent
CONFIG_PATH: Path = BASE_DIR / "config.json"
