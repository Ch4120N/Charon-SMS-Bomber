"""Reusable TUI widgets (modern palette)."""
from __future__ import annotations

from typing import Any, Optional

from rich.text import Text

from ui.theme import (
    PRIMARY, PRIMARY_ALT, ACCENT, OK, BAD, WARN,
    FG, FG_DIM, FG_MUTED,
)
from ui.tui import KEY_BACKSPACE, KEY_ENTER, KEY_LEFT, KEY_RIGHT


class TextInput:
    def __init__(self, value: str = "", mask: bool = False) -> None:
