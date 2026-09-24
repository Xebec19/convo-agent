from datetime import datetime

from database import Base
from models.user_model import User
from sqlalchemy import TIMESTAMP, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
        index=True,
    )
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
        ForeignKey("users.id"),
        nullable=True,
    )

    user: Mapped["User"] = relationship(back_populates="sessions")
