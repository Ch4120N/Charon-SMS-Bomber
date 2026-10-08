from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ui.theme import (
    PRIMARY, PRIMARY_ALT, ACCENT, OK, FG, FG_DIM, FG_MUTED,
    BORDER, BOX_MAIN,
)
from ui.tui import Screen, KEY_UP, KEY_DOWN, KEY_ENTER
from utils.version import NOTICE


_ITEMS = [
    ("start",    "Start Attack",       "launch a new SMS attack"),
    ("continue", "Resume Session",     "reuse last saved session"),
    ("settings", "Settings",           "edit config.json values"),
    ("apis",     "API Manager",        "browse, filter, reload APIs"),
    ("updates",  "Check for Updates",  "download latest apis.json"),
    ("logs",     "Live Logs",          "tail the runtime log file"),
    ("history",  "Session History",    "past attack results"),
    ("help",     "Help",               "strategies, hotkeys, concepts"),
    ("about",    "About",              "program info and credits"),
    ("exit",     "Exit",               "quit ChSMSBomber"),
]


class MainMenuScreen(Screen):
    name = "main_menu"
    title = "Home"
    hotkeys = {
        "s": "start", "r": "resume", "e": "settings",
        "a": "apis", "u": "updates", "l": "logs",
        "h": "history", "?": "help", "i": "about",
    }

    def __init__(self, app) -> None:
        super().__init__(app)
        self.cursor = 0

    def render(self) -> Panel:
        grid = Table.grid(padding=(0, 3))
        grid.add_column(width=2)
        grid.add_column(width=22)
        grid.add_column(ratio=1)

        for i, (_id, name, desc) in enumerate(_ITEMS):
            focused = i == self.cursor
            marker = Text("▌", style=f"bold {PRIMARY}") if focused else Text(" ")
            name_style = f"bold {PRIMARY_ALT}" if focused else FG
            desc_style = FG_DIM if focused else FG_MUTED
            grid.add_row(
                marker,
                Text(name, style=name_style),
                Text(desc, style=desc_style),
            )

        return Panel(
            Align.center(grid, vertical="middle"),
            title=f"[bold {PRIMARY}]  Main Menu  [/]",
            subtitle=f"[{FG_MUTED}]{NOTICE}[/]",
            border_style=BORDER, box=BOX_MAIN, padding=(1, 4),
        )

