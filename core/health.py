"""API health tracker — failure counting + cooldown."""
from __future__ import annotations

import threading
import time
from typing import Any

from core.apis import api_key


class ApiHealthTracker:
    def __init__(self, threshold: int, cooldown: int) -> None:
        self.threshold = max(1, int(threshold))
