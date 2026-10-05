"""Live log tail viewer."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from ui.theme import (
    PRIMARY, ACCENT, OK, WARN, BAD, FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
)
from ui.tui import Screen, KEY_UP, KEY_DOWN, KEY_ESC
from utils.paths import LOGS_DIR


_LEVEL_STYLE = {
    "DEBUG": FG_MUTED,
    "INFO": FG,
    "WARNING": WARN,
    "ERROR": BAD,
    "CRITICAL": f"bold {BAD}",
}


class LogsScreen(Screen):
    name = "logs"
