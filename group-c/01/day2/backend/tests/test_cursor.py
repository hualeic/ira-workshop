from app.utils.cursor import encode_cursor, decode_cursor
from datetime import datetime


def test_cursor_roundtrip():
    dt = datetime(2026, 4, 10, 8, 30, 0)
    msg_id = "abc-123-def"
    encoded = encode_cursor(dt, msg_id)
    assert isinstance(encoded, str)
    assert len(encoded) > 0

    decoded = decode_cursor(encoded)
    assert decoded is not None
    pub_at, mid = decoded
    assert pub_at == dt
    assert mid == msg_id


def test_cursor_invalid():
    result = decode_cursor("not-a-valid-cursor!!!")
    assert result is None


def test_cursor_empty():
    result = decode_cursor("")
    assert result is None
