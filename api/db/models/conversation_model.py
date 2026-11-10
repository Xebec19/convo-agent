import uuid
from datetime import datetime

from db.db import Base
from sqlalchemy import TIMESTAMP, Enum, text
from sqlalchemy.orm import Mapped, mapped_column


class Conversation(Base):
    __tablename__ = "conversations"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    created_on: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default="CURRENT_TIMESTAMP"
    )
    status: Mapped[str] = mapped_column(
        Enum("active", "inactive", name="status"),
        nullable=False,
        server_default="active",
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        # ForeignKey("users.id"),
        nullable=True,
    )
