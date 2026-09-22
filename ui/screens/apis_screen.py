from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.apis import load_apis
from ui.theme import (
    PRIMARY, API_COLOR, API_BRIGHT, OK, WARN, BAD,
    FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
)
from ui.tui import Screen, KEY_UP, KEY_DOWN, KEY_ENTER, KEY_ESC
from ui.widgets import TextInput


class ApisScreen(Screen):
    name = "apis"
    title = "API Manager"
    hotkeys = {"r": "reload", "/": "filter", "g/G": "jump"}

    def __init__(self, app) -> None:
        super().__init__(app)
        self.cursor = 0
        self.top = 0
        self.page_size = 20
        self.search = ""
        self._searching = False
        self._search_widget: Optional[TextInput] = None

    def _visible(self) -> list[dict]:
        if not self.search:
            return self.app.apis
        s = self.search.lower()
        return [
            a for a in self.app.apis
            if s in a.get("name", "").lower() or s in a.get("url", "").lower()
        ]

    def render_cache_key(self):
        return (self.cursor, self.top, self.search, len(self.app.apis))

    def render(self) -> Panel:
        items = self._visible()
        if self.cursor >= len(items):
            self.cursor = max(0, len(items) - 1)
        if self.cursor < self.top:
            self.top = self.cursor
        elif self.cursor >= self.top + self.page_size:
            self.top = self.cursor - self.page_size + 1

        info = Table.grid(padding=(0, 2))
        info.add_column(style=FG_MUTED)
        info.add_column(style=FG)
