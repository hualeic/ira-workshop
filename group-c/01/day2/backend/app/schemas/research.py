import json


def to_summary(message, is_read, highlight=None):
    result = {
        "messageId": message.id,
        "title": message.title,
        "summary": message.summary or "",
        "publishedAt": _format_dt(message.published_at),
        "sourceType": message.source_type,
        "sourceName": message.source_name,
        "category": message.category,
        "read": is_read,
    }
    if highlight is not None:
        result["highlight"] = highlight
    return result


def to_detail(message, is_read):
    result = to_summary(message, is_read)
    result["body"] = message.body
    result["contentFormat"] = message.content_format
    result["links"] = json.loads(message.links) if message.links else []
    result["metadata"] = json.loads(message.metadata_) if message.metadata_ else {}
    return result


def _format_dt(dt):
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
