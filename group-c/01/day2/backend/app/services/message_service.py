import html
import re
from datetime import datetime, timezone

from sqlalchemy import or_, and_, text

from app.extensions import db
from app.models.research import ResearchMessage, ResearchMessageRead
from app.schemas.research import to_summary, to_detail, _format_dt
from app.utils.cursor import encode_cursor, decode_cursor


def list_messages(cursor, limit, unread_only, category, source_type, user_id):
    query = ResearchMessage.query.filter(ResearchMessage.deleted_at.is_(None))

    if category:
        query = query.filter(ResearchMessage.category == category)
    if source_type:
        query = query.filter(ResearchMessage.source_type == source_type)
    if unread_only:
        subq = db.session.query(ResearchMessageRead.message_id).filter(
            ResearchMessageRead.user_id == user_id
        )
        query = query.filter(~ResearchMessage.id.in_(subq))

    if cursor:
        decoded = decode_cursor(cursor)
        if decoded is None:
            from app.utils.errors import ValidationError
            raise ValidationError("Invalid cursor")
        cursor_pub, cursor_id = decoded
        query = query.filter(
            or_(
                ResearchMessage.published_at < cursor_pub,
                and_(
                    ResearchMessage.published_at == cursor_pub,
                    ResearchMessage.id < cursor_id,
                ),
            )
        )

    query = query.order_by(
        ResearchMessage.published_at.desc(), ResearchMessage.id.desc()
    )
    messages = query.limit(limit + 1).all()

    has_more = len(messages) > limit
    items = messages[:limit]

    next_cursor = None
    if has_more and items:
        last = items[-1]
        next_cursor = encode_cursor(last.published_at, last.id)

    read_ids = _get_read_ids(user_id, [m.id for m in items])
    result_items = [to_summary(m, m.id in read_ids) for m in items]

    return {"items": result_items, "nextCursor": next_cursor, "hasMore": has_more}


def search_messages(q, from_date, to_date, cursor, limit, user_id):
    query = ResearchMessage.query.filter(ResearchMessage.deleted_at.is_(None))

    escaped_q = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    pattern = f"%{escaped_q}%"

    query = query.filter(
        or_(
            ResearchMessage.title.like(pattern),
            ResearchMessage.summary.like(pattern),
            ResearchMessage.body.like(pattern),
        )
    )

    if from_date:
        query = query.filter(ResearchMessage.published_at >= from_date)
    if to_date:
        query = query.filter(ResearchMessage.published_at <= to_date)

    if cursor:
        decoded = decode_cursor(cursor)
        if decoded is None:
            from app.utils.errors import ValidationError
            raise ValidationError("Invalid cursor")
        cursor_pub, cursor_id = decoded
        query = query.filter(
            or_(
                ResearchMessage.published_at < cursor_pub,
                and_(
                    ResearchMessage.published_at == cursor_pub,
                    ResearchMessage.id < cursor_id,
                ),
            )
        )

    query = query.order_by(
        ResearchMessage.published_at.desc(), ResearchMessage.id.desc()
    )
    messages = query.limit(limit + 1).all()

    has_more = len(messages) > limit
    items = messages[:limit]

    next_cursor = None
    if has_more and items:
        last = items[-1]
        next_cursor = encode_cursor(last.published_at, last.id)

    read_ids = _get_read_ids(user_id, [m.id for m in items])
    result_items = [
        to_summary(m, m.id in read_ids, highlight=_extract_highlight(m, q))
        for m in items
    ]

    return {"items": result_items, "nextCursor": next_cursor, "hasMore": has_more}


def get_message_detail(message_id, user_id):
    message = ResearchMessage.query.filter(
        ResearchMessage.id == message_id,
        ResearchMessage.deleted_at.is_(None),
    ).first()

    if message is None:
        return None

    is_read = (
        db.session.query(ResearchMessageRead)
        .filter(
            ResearchMessageRead.user_id == user_id,
            ResearchMessageRead.message_id == message_id,
        )
        .first()
        is not None
    )

    return to_detail(message, is_read)


def mark_read(message_id, user_id):
    message = ResearchMessage.query.filter(
        ResearchMessage.id == message_id,
        ResearchMessage.deleted_at.is_(None),
    ).first()

    if message is None:
        return None

    existing = ResearchMessageRead.query.filter(
        ResearchMessageRead.user_id == user_id,
        ResearchMessageRead.message_id == message_id,
    ).first()

    if existing is None:
        existing = ResearchMessageRead(
            user_id=user_id,
            message_id=message_id,
        )
        db.session.add(existing)
        db.session.commit()

    return {
        "messageId": message_id,
        "read": True,
        "readAt": _format_dt(existing.read_at),
    }


def _get_read_ids(user_id, message_ids):
    if not message_ids:
        return set()
    reads = (
        ResearchMessageRead.query.filter(
            ResearchMessageRead.user_id == user_id,
            ResearchMessageRead.message_id.in_(message_ids),
        )
        .all()
    )
    return {r.message_id for r in reads}


def _extract_highlight(message, query):
    q_lower = query.lower()
    for field in [message.title, message.summary or "", message.body]:
        idx = field.lower().find(q_lower)
        if idx >= 0:
            start = max(0, idx - 50)
            end = min(len(field), idx + len(query) + 50)
            snippet = field[start:end]
            prefix = "..." if start > 0 else ""
            suffix = "..." if end < len(field) else ""
            safe = html.escape(snippet)
            escaped_q = html.escape(query)
            highlighted = re.sub(
                re.escape(escaped_q),
                f"<em>{escaped_q}</em>",
                safe,
                count=1,
                flags=re.IGNORECASE,
            )
            return prefix + highlighted + suffix
    return None
