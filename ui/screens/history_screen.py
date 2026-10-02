"""Session history viewer."""
from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.history import clear_history, load_history
from ui.theme import (
    PRIMARY, ACCENT, OK, WARN, BAD, FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
)
from ui.tui import Screen, KEY_UP, KEY_DOWN, KEY_ESC, KEY_ENTER


class HistoryScreen(Screen):
    name = "history"
    title = "Session History"
    hotkeys = {"r": "reload", "c": "clear"}
