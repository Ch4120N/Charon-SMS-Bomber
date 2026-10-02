"""Help screen with working tab and scroll navigation."""
from __future__ import annotations

from typing import Any, Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.attacker import STRATEGIES
from ui.theme import (
    PRIMARY, PRIMARY_ALT, API_COLOR, ACCENT, OK, WARN, BAD,
    FG, FG_DIM, FG_MUTED, BORDER,
    BOX_MAIN,
)
from ui.tui import (
    Screen,
    KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT,
    KEY_ESC, KEY_ENTER, KEY_BACKSPACE,
)
from ui.widgets import TextInput


_SECTIONS = ["strategies", "concepts", "hotkeys", "config", "apis"]


class HelpScreen(Screen):
    name = "help"
    title = "Help"
    hotkeys = {"←→": "tab", "↑↓": "scroll", "/": "search"}

    def __init__(self, app) -> None:
        super().__init__(app)
        self.section_idx = 0
        self.scroll = 0
        self.search = ""
        self._searching = False
        self._search_widget: Optional[TextInput] = None

    @property
    def section(self) -> str:
        return _SECTIONS[self.section_idx]

    
    def render_cache_key(self) -> Any:
        return (self.section_idx, self.scroll, self.search, self._searching)

    
    def render(self) -> Panel:
        # Tabs
        tabs = Text("  ")
        for i, name in enumerate(_SECTIONS):
            label = name.upper()
            if i == self.section_idx:
                tabs.append(f" {label} ", style=f"bold black on {PRIMARY_ALT}")
            else:
                tabs.append(f" {label} ", style=FG_DIM)
            tabs.append("   ")

        # Search line
        search_line = Text()
        if self._searching:
            search_line.append("  filter: ", style=f"bold {PRIMARY}")
            search_line.append_text(self._search_widget.render(True, 40))  # type: ignore
        elif self.search:
            search_line.append(f"  filter: {self.search}",
                               style=f"bold {PRIMARY}")

        # Body
        body = self._render_section()

        # Scroll indicator (only if content taller than viewport)
        scroll_note = Text()
        if self.scroll > 0:
            scroll_note.append(f"  ↑ scrolled {self.scroll}", style=FG_MUTED)
        hint = Text()
        hint.append("  ", style=FG_MUTED)
        hint.append("← →", style=f"bold {OK}")
        hint.append(" switch tabs   ", style=FG_DIM)
        hint.append("↑ ↓", style=f"bold {OK}")
        hint.append(" scroll   ", style=FG_DIM)
        hint.append("/", style=f"bold {OK}")
        hint.append(" filter   ", style=FG_DIM)
        hint.append("Esc", style=f"bold {OK}")
        hint.append(" back", style=FG_DIM)

        return Panel(
            Align.left(Group(tabs, search_line, Text(""), body,
                             Text(""), scroll_note, hint),
                       vertical="top"),
            title=f"[bold {PRIMARY}]  Help  [/]",
            border_style=BORDER, box=BOX_MAIN, padding=(1, 2),
        )

    
    def _render_section(self):
        if self.section == "strategies":
