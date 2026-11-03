from datetime import datetime

from db.db import Base
from sqlalchemy import TIMESTAMP, Enum
from sqlalchemy.orm import Mapped, mapped_column


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_on: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default="CURRENT_TIMESTAMP"
    )
    status: Mapped[str] = mapped_column(
        Enum("active", "inactive", name="status"),
        nullable=False,
        server_default="active",
    )
    updated_on: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default="CURRENT_TIMESTAMP",
    )
    user_id: Mapped[int | None] = mapped_column(
        # ForeignKey("users.id"),
        nullable=True,
    )
