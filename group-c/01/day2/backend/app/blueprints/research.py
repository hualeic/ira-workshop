from flask import Blueprint, request, g, current_app, jsonify
from dateutil import parser as dateutil_parser

from app.services import message_service
from app.utils.errors import ValidationError, NotFoundError, RateLimitError
from app.utils.rate_limiter import check_rate_limit

research_bp = Blueprint("research", __name__, url_prefix="/api/v1/research")


@research_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "module": "M1", "version": "1.0.0"})


@research_bp.route("/messages", methods=["GET"])
def list_messages():
    cursor = request.args.get("cursor")
    limit = request.args.get("limit", current_app.config["DEFAULT_PAGE_LIMIT"], type=int)
    unread_only = request.args.get("unreadOnly", "false").lower() == "true"
    category = request.args.get("category")
    source_type = request.args.get("sourceType")

    if limit < 1 or limit > current_app.config["MAX_PAGE_LIMIT"]:
        raise ValidationError(
            f"limit must be between 1 and {current_app.config['MAX_PAGE_LIMIT']}",
            {"max_limit": current_app.config["MAX_PAGE_LIMIT"]},
        )

    result = message_service.list_messages(
        cursor=cursor,
        limit=limit,
        unread_only=unread_only,
        category=category,
        source_type=source_type,
        user_id=g.user_id,
    )
    return jsonify(result)


@research_bp.route("/messages/search", methods=["GET"])
def search_messages():
    q = (request.args.get("q") or "").strip()
    from_str = request.args.get("from")
    to_str = request.args.get("to")
    cursor = request.args.get("cursor")
    limit = request.args.get("limit", current_app.config["DEFAULT_PAGE_LIMIT"], type=int)

    max_len = current_app.config["SEARCH_QUERY_MAX_LENGTH"]
    if not q or len(q) < 1:
        raise ValidationError("Search query 'q' is required and must be non-empty")
    if len(q) > max_len:
        raise ValidationError(
            f"Search query 'q' must be at most {max_len} characters",
            {"max_length": max_len},
        )
    if limit < 1 or limit > current_app.config["MAX_PAGE_LIMIT"]:
        raise ValidationError(
            f"limit must be between 1 and {current_app.config['MAX_PAGE_LIMIT']}"
        )

    allowed = check_rate_limit(
        g.user_id,
        current_app.config["RATE_LIMIT_SEARCH_MAX"],
        current_app.config["RATE_LIMIT_SEARCH_WINDOW_SECONDS"],
    )
    if not allowed:
        raise RateLimitError(
            f"Search rate limit exceeded. Maximum {current_app.config['RATE_LIMIT_SEARCH_MAX']} "
            f"requests per {current_app.config['RATE_LIMIT_SEARCH_WINDOW_SECONDS']} seconds."
        )

    from_date = None
    to_date = None
    if from_str:
        try:
            from_date = dateutil_parser.isoparse(from_str)
        except (ValueError, TypeError):
            raise ValidationError("Invalid 'from' date format. Use ISO-8601.")
    if to_str:
        try:
            to_date = dateutil_parser.isoparse(to_str)
        except (ValueError, TypeError):
            raise ValidationError("Invalid 'to' date format. Use ISO-8601.")

    result = message_service.search_messages(
        q=q,
        from_date=from_date,
        to_date=to_date,
        cursor=cursor,
        limit=limit,
        user_id=g.user_id,
    )
    return jsonify(result)


@research_bp.route("/messages/<message_id>", methods=["GET"])
def get_message_detail(message_id):
    result = message_service.get_message_detail(message_id, g.user_id)
    if result is None:
        raise NotFoundError("Message not found or has been deleted")
    return jsonify(result)


@research_bp.route("/messages/<message_id>/read", methods=["PATCH"])
def mark_message_read(message_id):
    result = message_service.mark_read(message_id, g.user_id)
    if result is None:
        raise NotFoundError("Message not found or has been deleted")
    return jsonify(result)
