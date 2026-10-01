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

    def __init__(self, app) -> None:
        super().__init__(app)
        self.entries = []
        self.cursor = 0
        self.top = 0
        self.page_size = 18

    def on_enter(self) -> None:
        self.entries = load_history()
        self.cursor = max(0, len(self.entries) - 1)
        self.top = max(0, len(self.entries) - self.page_size)

    def render_cache_key(self):
        return (self.cursor, self.top, len(self.entries))

    def render(self) -> Panel:
        if not self.entries:
            return Panel(
                Align.center(Text("\n  no sessions yet\n", style=FG_MUTED),
                             vertical="middle"),
                title=f"[bold {PRIMARY}]  Session History  [/]",
                border_style=BORDER, box=BOX_MAIN, padding=(1, 2),
            )

        if self.cursor < self.top:
            self.top = self.cursor
        elif self.cursor >= self.top + self.page_size:
            self.top = self.cursor - self.page_size + 1

        t = Table(
            box=None, show_header=True, header_style=f"bold {PRIMARY}",
            padding=(0, 1), expand=True,
        )
        t.add_column("", width=2)
        t.add_column("When", style=FG_DIM, width=20)
        t.add_column("Strategy", style=ACCENT, width=12)
        t.add_column("Targets", style=FG, overflow="fold")
        t.add_column("Sent", justify="right", style=FG_DIM)
        t.add_column("OK", justify="right", style=OK)
        t.add_column("Fail", justify="right", style=BAD)
        t.add_column("Rate", justify="right", style=WARN)

        for i in range(self.top, min(self.top + self.page_size, len(self.entries))):
            e = self.entries[i]
            focused = i == self.cursor
            t.add_row(
                "▌" if focused else " ",
                e.ts.replace("T", " "),
                e.strategy,
                ", ".join(e.targets)[:40],
                str(e.sent),
                str(e.success),
                str(e.failed),
                f"{e.rate:.1f}%",
            )

        detail = Text()
        if self.entries:
            e = self.entries[self.cursor]
            detail.append("\n  elapsed: ", style=FG_MUTED)
            detail.append(f"{e.elapsed}s", style=FG)
            detail.append("   threads: ", style=FG_MUTED)
            detail.append(str(e.threads), style=FG)
            detail.append("   rounds: ", style=FG_MUTED)
            detail.append(str(e.rounds), style=FG)

        foot = Text()
        foot.append("\n  ", style=FG_MUTED)
        foot.append("↑ ↓", style=f"bold {OK}")
        foot.append(" scroll   ", style=FG_DIM)
        foot.append("r", style=f"bold {OK}")
        foot.append(" reload   ", style=FG_DIM)
        foot.append("c", style=f"bold {OK}")
        foot.append(" clear history   ", style=FG_DIM)
        foot.append("Esc", style=f"bold {OK}")
        foot.append(" back", style=FG_DIM)

        return Panel(
            Align.left(Group(t, detail, foot), vertical="top"),
            title=f"[bold {PRIMARY}]  Session History  [/]",
            subtitle=f"[{FG_MUTED}]{len(self.entries)} entries[/]",
            border_style=BORDER, box=BOX_MAIN, padding=(1, 2),
        )

    def handle_key(self, key: str) -> Optional[str]:
        if key in (KEY_UP, "k"):
            if self.entries:
                self.cursor = (self.cursor - 1) % len(self.entries)
            return None
