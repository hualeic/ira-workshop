import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MOCK_USER_ID = "00000000-0000-0000-0000-000000000001"
    RATE_LIMIT_SEARCH_MAX = 30
    RATE_LIMIT_SEARCH_WINDOW_SECONDS = 60
    DEFAULT_PAGE_LIMIT = 20
    MAX_PAGE_LIMIT = 100
    SEARCH_QUERY_MAX_LENGTH = 200


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "research.db")


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    RATE_LIMIT_SEARCH_MAX = 999


config_map = {
    "dev": DevConfig,
    "testing": TestingConfig,
}
