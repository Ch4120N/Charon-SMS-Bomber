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
        self.value = value
        self.cursor = len(value)
        self.mask = mask

    def handle(self, key: str) -> Optional[str]:
        from ui.tui import KEY_ENTER, KEY_BACKSPACE, KEY_LEFT, KEY_RIGHT
        if key == KEY_ENTER:
            return self.value
        if key == KEY_BACKSPACE:
            if self.cursor > 0:
                self.value = self.value[: self.cursor - 1] + self.value[self.cursor :]
                self.cursor -= 1
            return None
        if key == KEY_LEFT:
            self.cursor = max(0, self.cursor - 1)
            return None
        if key == KEY_RIGHT:
            self.cursor = min(len(self.value), self.cursor + 1)
            return None
        if len(key) == 1 and key.isprintable():
            self.value = self.value[: self.cursor] + key + self.value[self.cursor :]
            self.cursor += 1
