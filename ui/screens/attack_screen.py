from __future__ import annotations

import threading
from pathlib import Path
from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.attacker import Attacker, STRATEGIES
from core.history import append_history, make_entry
from core.session import save_session
from core.stats import export_csv, export_html, export_json
from ui.theme import (
    PRIMARY, PRIMARY_ALT, API_COLOR, ACCENT, OK, WARN, BAD,
    FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN, SPINNER_BAR,
)
from ui.tui import Screen, KEY_ESC, KEY_ENTER, KEY_SPACE
from utils.paths import REPORTS_DIR
from utils.version import NOTICE


class AttackScreen(Screen):
    name = "attack"
    title = "Attack"
    hotkeys = {"space": "stop", "Esc": "stop/back", "s": "save reports"}
    show_spinner = True
    animating = True

    def __init__(
        self,
        app,
        targets: list[str],
        threads: int,
        rounds: int,
        delay: float,
        dry_run: bool = False,
    ) -> None:
        super().__init__(app)
        self.targets = targets
        self.threads = threads
        self.rounds = rounds
        self.delay = delay
        self.dry_run = dry_run

        self.attacker = Attacker(app.cfg, app.apis, app.logger)
        self.started = False
        self.finished = False
        self.reports_saved: list[Path] = []
        self.dry_run_report: Optional[dict] = None
        self._history_saved = False

    def on_enter(self) -> None:
        save_session(self.targets, self.threads, self.rounds, self.delay)
        if self.dry_run:
            self.dry_run_report = self.attacker.dry_run(self.targets)
            self.finished = True
            self.show_spinner = False
            self.animating = False
            self.app.notify("dry-run complete", style=OK)
            return
        self._start_thread()
        self.app.notify("attack running — Space to stop", style=WARN)

    def on_exit(self) -> None:
        self.attacker.stop_flag.set()

    def _start_thread(self) -> None:
        if self.started:
            return
        self.started = True

        def _run() -> None:
            try:
                self.attacker.run(
                    self.targets, self.threads, self.rounds, self.delay
                )
            finally:
                self.finished = True
                self.show_spinner = False
                self.animating = False
                self._save_history_once()
                self.app.notify("attack complete", style=OK)

        threading.Thread(target=_run, daemon=True).start()

    def _save_history_once(self) -> None:
        if self._history_saved or self.dry_run:
            return
        self._history_saved = True
        s = self.attacker.stats
        try:
            append_history(make_entry(
                targets=self.targets,
                strategy=self.attacker.strategy,
                threads=self.threads,
                rounds=self.rounds,
                sent=s.sent,
                success=s.success,
                failed=s.failed,
                elapsed=s.elapsed,
            ))
        except Exception:
            pass

    
    def render_cache_key(self):
        s = self.attacker.stats
        return (s.sent, s.success, s.failed, self.attacker.round_idx,
                self.finished, self.app.frame)

    def render(self) -> Panel:
        if self.dry_run and self.dry_run_report:
            return self._render_dry_run()

        atk = self.attacker
        stats = atk.stats

        rounds_label = (
            "unlimited" if atk.unlimited
            else f"{atk.round_idx} / {atk.total_rounds}"
        )
        strat = STRATEGIES.get(atk.strategy, {}).get("label", atk.strategy)

        header = Table.grid(padding=(0, 2))
        header.add_column(style=FG_MUTED)
        header.add_column(style=FG)
        header.add_row("Targets", ", ".join(self.targets))
        header.add_row("Strategy", strat)
        header.add_row("Threads", str(self.threads))
        header.add_row("Rounds", rounds_label)

        counters = Table.grid(expand=True)
        for _ in range(4):
            counters.add_column(justify="center")
        counters.add_row(
            f"[{FG_DIM}]Sent[/]\n[bold {PRIMARY}]{stats.sent}[/]",
            f"[{FG_DIM}]Success[/]\n[bold {OK}]{stats.success}[/]",
            f"[{FG_DIM}]Failed[/]\n[bold {BAD}]{stats.failed}[/]",
            f"[{FG_DIM}]Rate[/]\n[bold {WARN}]{stats.rate:.1f}%[/]",
        )

