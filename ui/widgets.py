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
        return None

    def render(self, focused: bool, width: int = 40) -> Text:
        from ui.theme import (
            FORM_VALUE, FORM_VALUE_FOCUSED, FORM_CURSOR_FG, FORM_CURSOR_BG,
            FORM_PLACEHOLDER, TEXT_DISABLED,
        )
        t = Text()
        before = self.value[: self.cursor]
        cur = self.value[self.cursor : self.cursor + 1] or " "
        after = self.value[self.cursor + 1 :]
        if self.mask:
            before = "*" * len(before)
            cur = "*" if cur != " " else " "
            after = "*" * len(after)

        if focused:
            t.append(before, style=FORM_VALUE_FOCUSED)
            t.append(cur, style=f"bold {FORM_CURSOR_FG} on {FORM_CURSOR_BG}")
            t.append(after, style=FORM_VALUE_FOCUSED)
            pad = max(0, width - len(before) - 1 - len(after))
            t.append(" " * pad, style=TEXT_DISABLED)
        else:
            if self.value:
                t.append(self.value, style=FORM_VALUE)
                pad = max(0, width - len(self.value))
            else:
                t.append("-", style=FORM_PLACEHOLDER)
                pad = max(0, width - 1)
            t.append(" " * pad, style=TEXT_DISABLED)
        return t


class Toggle:
    def __init__(self, value: bool) -> None:
        self.value = bool(value)

    def toggle(self) -> None:
        self.value = not self.value

    def render(self) -> Text:
        from ui.theme import (
            TOGGLE_ON_BG, TOGGLE_ON_FG, TOGGLE_OFF_BG, TOGGLE_OFF_FG,
        )
        if self.value:
            return Text(" ● ON  ", style=f"bold {TOGGLE_ON_FG} on {TOGGLE_ON_BG}")
        return Text(" ○ OFF ", style=f"bold {TOGGLE_OFF_FG} on {TOGGLE_OFF_BG}")


class Cycle:
