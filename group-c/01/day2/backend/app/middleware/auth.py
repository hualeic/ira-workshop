from flask import g, current_app


def mock_auth():
    g.user_id = current_app.config["MOCK_USER_ID"]
