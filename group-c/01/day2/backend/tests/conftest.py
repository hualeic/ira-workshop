import json
import uuid
import pytest
from datetime import datetime, timezone

from app import create_app
from app.extensions import db
from app.models.research import ResearchMessage, ResearchMessageRead
from app.utils.rate_limiter import reset_rate_limiter

MOCK_USER_ID = "00000000-0000-0000-0000-000000000001"


@pytest.fixture
def app():
    app = create_app("testing")
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_rate_limit():
    reset_rate_limiter()


@pytest.fixture
def seeded_db(app):
    with app.app_context():
        messages = []
        for i in range(15):
            msg = ResearchMessage(
                id=str(uuid.uuid4()),
                title=f"Test Message {i+1:02d}",
                summary=f"Summary for message {i+1}",
                body=f"Body content for message {i+1}. This contains some test keywords.",
                content_format="markdown",
                published_at=datetime(2026, 4, 1 + i, 8, 0, 0),
                category="宏观经济" if i % 3 == 0 else ("行业研究" if i % 3 == 1 else "个股分析"),
                source_type="manual" if i % 2 == 0 else "feed",
                source_name=f"Source {i+1}",
                links=json.dumps([{"label": "Link", "url": "https://example.com"}]) if i % 4 == 0 else None,
            )
            db.session.add(msg)
            messages.append(msg)

        db.session.flush()

        for j in [0, 1, 2]:
            read = ResearchMessageRead(
                user_id=MOCK_USER_ID,
                message_id=messages[j].id,
            )
            db.session.add(read)

        db.session.commit()
        yield messages
