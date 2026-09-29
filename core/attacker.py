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
