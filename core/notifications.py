"""Lightweight in-memory notification queue."""
from __future__ import annotations

import threading
import time
from collections import deque
