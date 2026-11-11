import uuid
from datetime import datetime

from db.db import Base
from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.conversation_id"),
        nullable=False,
    )

    created_on: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    user_role: Mapped[str] = mapped_column(
        ENUM("user", "ai", name="role", create_type=False),
        nullable=False,
        server_default="user",
    )
