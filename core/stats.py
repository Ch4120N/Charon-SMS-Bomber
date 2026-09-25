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
            "sent": stats.sent,
            "success": stats.success,
            "failed": stats.failed,
            "rate": round(stats.rate, 2),
        },
        "by_api": stats.by_api,
        "config_snapshot": {
            "threads": cfg["attack"]["threads"],
            "rounds": cfg["attack"]["rounds"],
            "delay": cfg["attack"]["delay"],
            "strategy": cfg["attack"]["strategy"],
        },
    }


def export_json(stats: Stats, targets: list[str], cfg: dict[str, Any]) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / f"report_{_stamp()}.json"
    path.write_text(
        json.dumps(_payload(stats, targets, cfg), indent=4, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def export_csv(stats: Stats, targets: list[str], cfg: dict[str, Any]) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / f"report_{_stamp()}.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["API", "Sent", "Success", "Failed"])
        for name, b in stats.by_api.items():
            w.writerow([name, b["sent"], b["success"], b["failed"]])
        w.writerow([])
        w.writerow(["TOTAL", stats.sent, stats.success, stats.failed])
    return path


def export_html(stats: Stats, targets: list[str], cfg: dict[str, Any]) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / f"report_{_stamp()}.html"
    rows = "\n".join(
        f"<tr><td>{html.escape(k)}</td><td>{v['sent']}</td>"
        f"<td class='ok'>{v['success']}</td>"
        f"<td class='bad'>{v['failed']}</td></tr>"
        for k, v in stats.by_api.items()
    )
    doc = f"""<!doctype html>
<html><head><meta charset="utf-8"/>
<title>{APP_NAME} report</title>
<style>
 body {{ font-family: system-ui, sans-serif; background:#0f1116; color:#e6e6e6; padding:32px; }}
 h1 {{ color:#5fd6ff; margin-bottom:4px; }}
 .meta {{ color:#888; margin-bottom:20px; }}
 table {{ border-collapse: collapse; width:100%; max-width:900px; }}
 th,td {{ padding:8px 12px; border-bottom:1px solid #222; text-align:left; }}
 th {{ color:#5fd6ff; }}
 .ok {{ color:#6ee787; }} .bad {{ color:#ff6b6b; }}
 .totals {{ margin-top:20px; font-size:1.1em; }}
</style></head><body>
<h1>{APP_NAME} v{APP_VERSION} — attack report</h1>
<div class="meta">{datetime.now().isoformat()} · targets: {html.escape(", ".join(targets))}</div>
<table>
 <thead><tr><th>API</th><th>Sent</th><th>Success</th><th>Failed</th></tr></thead>
 <tbody>{rows}</tbody>
</table>
<div class="totals">
 <b>Total sent:</b> {stats.sent} ·
 <b>Success:</b> <span class="ok">{stats.success}</span> ·
 <b>Failed:</b> <span class="bad">{stats.failed}</span> ·
 <b>Rate:</b> {stats.rate:.2f}% ·
 <b>Elapsed:</b> {stats.elapsed:.1f}s
</div>
</body></html>"""
