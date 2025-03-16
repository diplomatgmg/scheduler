from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(DeclarativeBase, AsyncAttrs):
    pass


class AdminChannel(Base):
    __tablename__ = "admin_channels"
    chat_id: Mapped[int] = mapped_column(primary_key=True)
    chat_title: Mapped[str] = mapped_column()
