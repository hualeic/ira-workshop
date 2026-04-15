import time
from collections import defaultdict

_buckets = defaultdict(list)


def check_rate_limit(user_id, max_requests, window_seconds):
    now = time.time()
    timestamps = _buckets[user_id]
    _buckets[user_id] = [t for t in timestamps if now - t < window_seconds]
    if len(_buckets[user_id]) >= max_requests:
        return False
    _buckets[user_id].append(now)
    return True


def reset_rate_limiter():
    _buckets.clear()
