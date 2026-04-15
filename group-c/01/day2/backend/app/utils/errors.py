import uuid
from datetime import datetime, timezone

from flask import abort, jsonify, request, g
from functools import wraps


class APIError(Exception):
    def __init__(self, http_status, code, message, details=None):
        self.http_status = http_status
        self.code = code
        self.message = message
        self.details = details or {}


class ValidationError(APIError):
    def __init__(self, message, details=None):
        super().__init__(400, "M1_VALIDATION_ERROR", message, details)


class NotFoundError(APIError):
    def __init__(self, message="Message not found"):
        super().__init__(404, "M1_MESSAGE_NOT_FOUND", message)


class RateLimitError(APIError):
    def __init__(self, message="Search rate limit exceeded"):
        super().__init__(429, "M1_RATE_LIMIT", message)


def generate_trace_id():
    return "trace_" + uuid.uuid4().hex[:16]


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(e):
        trace_id = getattr(g, "trace_id", generate_trace_id())
        resp = jsonify({
            "error": {
                "code": e.code,
                "message": e.message,
                "traceId": trace_id,
                "details": e.details,
            }
        })
        resp.status_code = e.http_status
        return resp

    @app.errorhandler(404)
    def handle_404(e):
        trace_id = getattr(g, "trace_id", generate_trace_id())
        return jsonify({
            "error": {
                "code": "M1_MESSAGE_NOT_FOUND",
                "message": "Resource not found",
                "traceId": trace_id,
                "details": {},
            }
        }), 404

    @app.errorhandler(405)
    def handle_405(e):
        trace_id = getattr(g, "trace_id", generate_trace_id())
        return jsonify({
            "error": {
                "code": "M1_VALIDATION_ERROR",
                "message": "Method not allowed",
                "traceId": trace_id,
                "details": {},
            }
        }), 405

    @app.errorhandler(500)
    def handle_500(e):
        trace_id = getattr(g, "trace_id", generate_trace_id())
        app.logger.error(f"[{trace_id}] Internal error: {e}")
        return jsonify({
            "error": {
                "code": "M1_INTERNAL_ERROR",
                "message": "Internal server error",
                "traceId": trace_id,
                "details": {},
            }
        }), 500
