import uuid
from datetime import datetime, timezone

from app.extensions import db


class ResearchMessage(db.Model):
    __tablename__ = "research_messages"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(500), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=False)
    content_format = db.Column(db.String(16), nullable=False, default="markdown")
    published_at = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(64), nullable=True)
    source_type = db.Column(db.String(32), nullable=True)
    source_name = db.Column(db.String(128), nullable=True)
    source_system = db.Column(db.String(64), nullable=True)
    external_ref = db.Column(db.String(256), nullable=True)
    links = db.Column(db.Text, nullable=True)  # JSON string
    metadata_ = db.Column("metadata", db.Text, nullable=True)  # JSON string
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        db.Index("idx_published_id", published_at.desc(), id.desc()),
        db.Index("idx_category", category),
    )


class ResearchMessageRead(db.Model):
    __tablename__ = "research_message_reads"

    user_id = db.Column(db.String(36), primary_key=True)
    message_id = db.Column(
        db.String(36),
        db.ForeignKey("research_messages.id", ondelete="CASCADE"),
        primary_key=True,
    )
    read_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
