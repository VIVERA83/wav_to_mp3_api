"""Модели сервиса Авторизации (AUTH)"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, Column, String, ForeignKey, BINARY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import EmailType

from store.database.database import Base


class UserModel(Base):
    """User model."""
    __tablename__ = "users"  # noqa

    id: Mapped[uuid4] = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_name: Mapped[str] = Column(String(100), nullable=False, unique=True)
    email: Mapped[str] = Column(EmailType, nullable=False)
    token: Mapped[uuid4] = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    create_date: datetime = Column(TIMESTAMP, default=datetime.now())
    modified_date: datetime = Column(TIMESTAMP, default=datetime.now())

    mp3: Mapped[list["Mp3Model"]] = relationship(cascade="all, delete-orphan")


class Mp3Model(Base):
    """Модель, Mp3."""
    __tablename__ = "users"  # noqa

    id: Mapped[uuid4] = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    mp3: Mapped[bytes] = Column(BINARY)
    file_name: Mapped[str] = Column(String(100))

    user_id: Mapped[uuid4] = mapped_column(ForeignKey("users.id"))
