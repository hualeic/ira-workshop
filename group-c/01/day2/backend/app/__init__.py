import os

from flask import Flask, g
from flask_cors import CORS

from app.config import config_map
from app.extensions import db
from app.utils.errors import generate_trace_id, register_error_handlers
from app.middleware.auth import mock_auth


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "dev")

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)

    @app.before_request
    def before_request():
        g.trace_id = generate_trace_id()
        mock_auth()

    register_error_handlers(app)

    from app.blueprints.research import research_bp
    app.register_blueprint(research_bp)

    with app.app_context():
        db.create_all()

    return app
