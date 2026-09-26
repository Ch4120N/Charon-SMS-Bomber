from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.attacker import STRATEGIES
from core.phone import parse_targets
from core.session import load_session
from ui.theme import (
    PRIMARY, PRIMARY_ALT, ACCENT, OK, WARN, BAD,
    FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
)
from ui.tui import (
    Screen, KEY_UP, KEY_DOWN, KEY_ENTER, KEY_ESC, KEY_SPACE,
    KEY_LEFT, KEY_RIGHT,
)
from ui.widgets import Field


class StartScreen(Screen):
    name = "start"
    title = "New Attack"
    hotkeys = {"⏎": "edit", "space": "toggle", "/": "help"}

    def __init__(self, app, mode: str = "new") -> None:
        super().__init__(app)
        self.mode = mode
        cfg = app.cfg["attack"]

        targets_val = ""
        threads_val = str(cfg["threads"])
        rounds_val = str(cfg["rounds"])
        delay_val = str(cfg["delay"])
        strategy_val = cfg["strategy"]

        if mode == "resume":
            data = load_session()
            if data:
                targets_val = ";".join(data["targets"])
                threads_val = str(data["threads"])
                rounds_val = str(data["rounds"])
                delay_val = str(data["delay"])

        self.fields: list[Field] = [
            Field("targets", "Targets", "text", targets_val,
                  hint="sep ';'  e.g. 0912...;0935..."),
            Field("threads", "Threads", "int", threads_val),
            Field("rounds", "Rounds", "int", rounds_val,
                  hint="0 = unlimited"),
            Field("delay", "Delay (s)", "float", delay_val),
            Field("strategy", "Strategy", "cycle", strategy_val,
                  choices=list(STRATEGIES.keys())),
            Field("dry_run", "Dry-run (no send)", "bool", cfg.get("dry_run", False)),
            Field("go", "START ATTACK", "action", None),
            Field("back", "Back to menu", "action", None),
        ]
        self.cursor = 0
        self.editing = False

    def render(self) -> Panel:
        strat = self.fields[4].widget.value  # type: ignore
        info = STRATEGIES.get(strat, {})

        rows = Table.grid(padding=(0, 2))
        rows.add_column(ratio=1)

        header = Text()
        header.append("  Target Setup\n", style=f"bold {ACCENT}")
        header.append("  ↑ ↓ move   ⏎ edit/activate   ← → change   Esc back\n",
                      style=FG_MUTED)
        rows.add_row(header)
        rows.add_row(Text(""))

        for i, f in enumerate(self.fields):
            rows.add_row(f.render(i == self.cursor))

        desc = Text()
        desc.append("\n  Strategy: ", style=FG_DIM)
        desc.append(f"{info.get('label', strat)}", style=f"bold {ACCENT}")
        desc.append(f"  —  {info.get('summary', '')}\n", style=FG)
        desc.append("  ", style=FG_DIM)
        desc.append(info.get("details", ""), style=FG_MUTED)
        desc.append("\n  Press ", style=FG_MUTED)
        desc.append("/", style=f"bold {OK}")
        desc.append(" to open the full help.", style=FG_MUTED)

        return Panel(
            Align.left(Group(rows, desc), vertical="top"),
            title=f"[bold {PRIMARY}]  {self.title}  [/]",
            border_style=BORDER, box=BOX_MAIN, padding=(1, 2),
        )

    def handle_key(self, key: str) -> Optional[str]:
        field = self.fields[self.cursor]

        if self.editing:
            if key == KEY_ESC:
                self.editing = False
                return None
            result = field.widget.handle(key)  # type: ignore
            if result is not None:
                if field.kind in ("int", "float") and not _valid_number(result, field.kind):
                    self.app.notify(f"invalid {field.kind}: {result!r}", style=BAD)
                    return None
                field.widget.value = result  # type: ignore
                self.editing = False
            return None

        if key in (KEY_UP, "k"):
            self.cursor = (self.cursor - 1) % len(self.fields)
            return None
        if key in (KEY_DOWN, "j"):
            self.cursor = (self.cursor + 1) % len(self.fields)
            return None
        if key == KEY_ESC:
            return "back"
