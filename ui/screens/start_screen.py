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
