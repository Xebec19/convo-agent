from datetime import datetime
from enum import Enum as PyEnum

from db.db import Base
from sqlalchemy import TIMESTAMP, Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class Status(str, PyEnum):
    active = "active"
    inactive = "inactive"


class Asset(Base):
    __tablename__ = "assets"

    asset_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    asset_key: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_on: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default="CURRENT_TIMESTAMP",
    )

    is_ingested: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    updated_on: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default="CURRENT_TIMESTAMP",
    )

    status: Mapped[Status] = mapped_column(
        Enum(Status, name="status"),
        nullable=False,
        server_default="active",
    )

    user_id: Mapped[int | None] = mapped_column(
        # ForeignKey("users.id"),
        nullable=True,
    )
