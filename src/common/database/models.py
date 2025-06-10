from typing import Any

from sqlalchemy import JSON, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    registry,
    relationship,
)


__all__ = [
    "Base",
    "ChannelModel",
    "DelayedMessageModel",
    "UserModel",
]


mapper_registry = registry()


class Base(DeclarativeBase, AsyncAttrs):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]

    timezone_offset: Mapped[int | None] = mapped_column(nullable=True)

    channels = relationship("ChannelModel", back_populates="user", cascade="all, delete")


class ChannelModel(Base):
    __tablename__ = "channels"
    __table_args__ = (UniqueConstraint("user_id", "chat_id", name="unique_user_chat"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str]
    chat_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str | None]

    user = relationship("UserModel", back_populates="channels")


class DelayedMessageModel(Base):
    __tablename__ = "delayed_messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    to_chat_id: Mapped[int] = mapped_column(BigInteger)
    is_sent: Mapped[bool] = mapped_column(default=False)
    message_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
