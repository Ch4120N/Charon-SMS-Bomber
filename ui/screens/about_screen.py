from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ui.theme import (
    PRIMARY, ACCENT, OK, BAD, FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
)
from ui.tui import Screen, KEY_ESC, KEY_ENTER
from utils.paths import APIS_PATH, CONFIG_PATH
from utils.version import (
    APP_AUTHOR, APP_LICENSE, APP_NAME, APP_REPO, APP_VERSION, NOTICE,
)


class AboutScreen(Screen):
    name = "about"
    title = "About"
    hotkeys = {"o": "open repo"}

    def render(self) -> Panel:
        t = Table.grid(padding=(0, 2))
        t.add_column(style=FG_MUTED, justify="right")
        t.add_column(style=FG)
        t.add_row("Program", APP_NAME)
        t.add_row("Version", APP_VERSION)
        t.add_row("Author", APP_AUTHOR)
        t.add_row("Repository", f"[underline {ACCENT}]{APP_REPO}[/]")
        t.add_row("License", APP_LICENSE)
        t.add_row("Config", str(CONFIG_PATH))
        t.add_row("APIs", str(APIS_PATH))
        t.add_row("Notice", f"[bold {BAD}]{NOTICE}[/]")

        head = Text("\n  About\n\n", style=f"bold {ACCENT}")
        foot = Text("\n  press o to open the repository in your browser\n",
                    style=FG_MUTED)

        return Panel(
            Align.left(Group(head, t, foot), vertical="top"),
            title=f"[bold {PRIMARY}]  About  [/]",
