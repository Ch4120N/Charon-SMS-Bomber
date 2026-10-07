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
