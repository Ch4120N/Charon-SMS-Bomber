"""Attack statistics + report exporters."""
from __future__ import annotations

import csv
import html
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from utils.paths import REPORTS_DIR
from utils.version import APP_NAME, APP_VERSION


@dataclass
class Stats:
    sent: int = 0
    success: int = 0
    failed: int = 0
    by_api: dict[str, dict[str, int]] = field(default_factory=dict)
    recent: list[tuple[str, str, bool]] = field(default_factory=list)
    start_ts: float = field(default_factory=time.time)

    def record(self, api_name: str, target: str, ok: bool) -> None:
        self.sent += 1
        self.success += int(ok)
        self.failed += int(not ok)
        b = self.by_api.setdefault(api_name, {"sent": 0, "success": 0, "failed": 0})
        b["sent"] += 1
        b["success" if ok else "failed"] += 1
        self.recent.append((api_name, target, ok))
        if len(self.recent) > 12:
            self.recent = self.recent[-12:]

    @property
    def elapsed(self) -> float:
        return time.time() - self.start_ts

    @property
    def rate(self) -> float:
        return (self.success / self.sent * 100) if self.sent else 0.0


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _payload(stats: Stats, targets: list[str], cfg: dict[str, Any]) -> dict[str, Any]:
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "timestamp": datetime.now().isoformat(),
        "targets": targets,
        "elapsed_seconds": round(stats.elapsed, 2),
        "totals": {
