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
        info.add_row("Total", str(len(self.app.apis)))
        info.add_row("Enabled",
                     str(sum(1 for a in self.app.apis if a.get("enabled", True))))
        if self.search:
            info.add_row("Filter", f"'{self.search}' → {len(items)} matches")

        search_line = Text()
        if self._searching:
            search_line.append("  filter: ", style=f"bold {API_BRIGHT}")
            search_line.append_text(self._search_widget.render(True, 40))  # type: ignore
        elif self.search:
            search_line.append(f"  filter: {self.search}",
                               style=f"bold {API_BRIGHT}")

        lst = Table(
            box=None, show_header=True, header_style=f"bold {API_BRIGHT}",
            padding=(0, 1), expand=True,
        )
        lst.add_column("", width=2)
        lst.add_column("#", width=4, justify="right", style=FG_MUTED)
        lst.add_column("Name", style=API_COLOR, no_wrap=True, width=22)
        lst.add_column("Method", width=6, style=WARN)
        lst.add_column("Tags", width=14, style=FG_DIM)
        lst.add_column("URL", style=FG, overflow="fold")

        for i in range(self.top, min(self.top + self.page_size, len(items))):
            api = items[i]
            focused = i == self.cursor
            lst.add_row(
                "▌" if focused else " ",
                str(i + 1),
                api.get("name", "?"),
                api.get("method", "POST"),
                ",".join(api.get("tags", []))[:12] or "-",
                api.get("url", "?"),
            )

        detail = Text()
        if items:
            api = items[self.cursor]
            detail.append("\n  Headers: ", style=FG_MUTED)
            hdrs = api.get("headers") or {}
            detail.append(", ".join(list(hdrs.keys())[:6]) if hdrs else "(none)",
                          style=FG)
            detail.append("   weight: ", style=FG_MUTED)
            detail.append(str(api.get("weight", 1)), style=FG)
            detail.append("   enabled: ", style=FG_MUTED)
            detail.append("yes" if api.get("enabled", True) else "no",
                          style=OK if api.get("enabled", True) else BAD)

