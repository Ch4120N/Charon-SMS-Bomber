"""Lightweight in-memory notification queue."""
from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Optional


@dataclass
class Toast:
    text: str
    style: str = "white"
    ttl: float = 3.5
    created: float = field(default_factory=time.time)

    @property
    def expired(self) -> bool:
        return time.time() - self.created > self.ttl


class NotificationCenter:
    def __init__(self, max_visible: int = 3) -> None:
        self._items: Deque[Toast] = deque(maxlen=10)
        self._lock = threading.Lock()
        self.max_visible = max_visible

