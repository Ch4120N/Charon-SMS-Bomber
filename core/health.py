"""API health tracker — failure counting + cooldown."""
from __future__ import annotations

import threading
import time
from typing import Any

from core.apis import api_key


class ApiHealthTracker:
    def __init__(self, threshold: int, cooldown: int) -> None:
        self.threshold = max(1, int(threshold))
        self.cooldown = max(1, int(cooldown))
        self._lock = threading.Lock()
        self._state: dict[str, dict[str, float]] = {}

    def is_available(self, api: dict[str, Any]) -> bool:
        with self._lock:
            st = self._state.get(api_key(api))
            if not st:
                return True
            if st.get("disabled_until", 0) > time.time():
                return False
            self._state.pop(api_key(api), None)
            return True

    def remaining_cooldown(self, api: dict[str, Any]) -> float:
        with self._lock:
            st = self._state.get(api_key(api))
            if not st:
