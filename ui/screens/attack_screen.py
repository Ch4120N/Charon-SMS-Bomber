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

        bar_len = 46
        if atk.unlimited:
            frame = self.app.frame
            pos = frame % (bar_len * 2)
            head = pos if pos < bar_len else bar_len * 2 - pos
            bar = Text("  ")
            for i in range(bar_len):
                if abs(i - head) <= 4:
                    bar.append("█", style=f"bold {OK}")
                elif abs(i - head) <= 7:
                    bar.append("▓", style=OK)
                else:
                    bar.append("░", style=FG_MUTED)
            bar.append(f"   elapsed {int(stats.elapsed)}s", style=FG_DIM)
        else:
            pct = (
                atk.round_idx / atk.total_rounds * 100
                if atk.total_rounds else 0
            )
            filled = int(bar_len * pct / 100)
            bar = Text("  ")
            bar.append("█" * filled, style=f"bold {OK}")
            bar.append("░" * (bar_len - filled), style=FG_MUTED)
            bar.append(f"  {pct:5.1f}%   elapsed {int(stats.elapsed)}s", style=FG_DIM)

        api_tbl = Table(
            title=f"[bold {API_COLOR}]  API Health  [/]",
            box=None, show_edge=False, expand=True, padding=(0, 1),
        )
        api_tbl.add_column("API", style=API_COLOR, no_wrap=True)
        api_tbl.add_column("Sent", justify="right", style=FG)
        api_tbl.add_column("OK", justify="right", style=OK)
        api_tbl.add_column("Fail", justify="right", style=BAD)
        api_tbl.add_column("Weight", justify="right", style=ACCENT)
        api_tbl.add_column("Status", style=WARN)

        by_name = {a.get("name"): a for a in atk.apis}
        rows = list(stats.by_api.items())[-12:]
        for name, b in rows:
            status = f"[{OK}]active[/]"
            if atk.health and name in by_name:
                rem = atk.health.remaining_cooldown(by_name[name])
                if rem > 0:
                    status = f"[{BAD}]cooling {int(rem)}s[/]"
            weight = ""
            if atk.strategy == "smart":
                with atk._weights_lock:  # type: ignore
                    weight = f"{atk._weights.get(name, 1.0):.2f}"  # type: ignore
            api_tbl.add_row(
                name,
                str(b.get("sent", 0)),
                str(b.get("success", 0)),
                str(b.get("failed", 0)),
                weight,
                status,
            )
        if not rows:
            api_tbl.add_row(f"[{FG_MUTED}]- no data yet -[/]", "", "", "", "", "")

        footer = Text()
        if self.finished:
            footer.append("\n  ✓ attack complete.  ", style=f"bold {OK}")
            footer.append("s = save reports   Esc = return", style=FG_DIM)
        else:
            footer.append("\n  ⠿ running...  ", style=f"bold {WARN}")
            footer.append("Space / Esc to stop", style=FG_DIM)
        footer.append(f"\n  {NOTICE}", style=FG_MUTED)

        return Panel(
            Align.left(
                Group(header, Text(""), counters, bar, Text(""), api_tbl, footer),
                vertical="top",
            ),
            title=f"[bold {PRIMARY}]  Attack in progress  [/]",
            border_style=BORDER, box=BOX_MAIN, padding=(1, 2),
        )

    def _render_dry_run(self) -> Panel:
        r = self.dry_run_report or {}
        t = Table.grid(padding=(0, 2))
        t.add_column(style=FG_MUTED)
        t.add_column(style=FG)
        t.add_row("Targets", ", ".join(r.get("targets", [])))
        t.add_row("APIs", str(r.get("apis", 0)))
        t.add_row("Strategy", r.get("strategy", ""))
        t.add_row("Jobs / round", str(r.get("jobs_per_round", 0)))
        t.add_row("Rounds", str(r.get("rounds", 0)))
        t.add_row("Total requests", str(r.get("total_requests", 0)))
        t.add_row("Threads", str(r.get("threads", 0)))
        rate = r.get("rate_limit", 0)
        t.add_row("Rate cap", f"{rate}/s" if rate else "off")

        return Panel(
            Align.left(Group(
                Text("\n  DRY RUN — no requests were sent.\n\n",
                     style=f"bold {WARN}"),
                t,
                Text("\n  Press s to save, Esc to return.\n", style=FG_MUTED),
            ), vertical="top"),
            title=f"[bold {PRIMARY}]  Dry Run  [/]",
            border_style=BORDER, box=BOX_MAIN, padding=(1, 2),
        )
    
    def handle_key(self, key: str) -> Optional[str]:
        if key == "s":
            self._save_reports()
            return None
        if key == KEY_SPACE and not self.finished:
            self.attacker.stop_flag.set()
            self.app.notify("stopping…", style=WARN)
            return None
        if key == KEY_ESC:
            if not self.finished:
                self.attacker.stop_flag.set()
            return "back"
        if key == KEY_ENTER and self.finished:
            return "back"
        return None

    def _save_reports(self) -> None:
        if not self.attacker.stats.sent and not self.dry_run:
            self.app.notify("no data to save", style=WARN)
            return
        try:
            REPORTS_DIR.mkdir(exist_ok=True)
            cfg = self.app.cfg
            fmt = cfg["output"]["report_format"].lower()
            if fmt == "csv":
