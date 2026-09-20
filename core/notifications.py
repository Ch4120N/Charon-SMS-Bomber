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
