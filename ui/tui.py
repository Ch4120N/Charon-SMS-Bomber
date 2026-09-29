"""Full-screen TUI engine with adaptive refresh and notifications."""
from __future__ import annotations

import queue
import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

