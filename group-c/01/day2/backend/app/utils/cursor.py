import base64
from datetime import datetime, timezone


def encode_cursor(published_at, message_id):
    if isinstance(published_at, datetime):
        ts = published_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        ts = str(published_at)
    raw = f"{ts}|{message_id}"
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def decode_cursor(cursor_str):
    try:
        padding = 4 - len(cursor_str) % 4
        if padding != 4:
            cursor_str += "=" * padding
        raw = base64.urlsafe_b64decode(cursor_str.encode()).decode()
        parts = raw.split("|", 1)
        if len(parts) != 2:
            return None
        ts_str, message_id = parts
        published_at = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return published_at, message_id
    except Exception:
        return None
