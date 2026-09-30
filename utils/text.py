from __future__ import annotations

import random
import string


def rand_id(n: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


def humanize_seconds(s: float) -> str:
    s = int(max(0, s))
    if s < 60:
        return f"{s}s"
    m, sec = divmod(s, 60)
    if m < 60:
