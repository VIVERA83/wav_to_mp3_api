"""Модели сервиса Авторизации (AUTH)"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy_utils import EmailType
from store.database.database import Base


class UserModel(Base):
    """User model."""
    __tablename__ = "users"  # noqa
    __table_args__ = {'extend_existing': True}

    id: Mapped[uuid4] = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_name: Mapped[str] = Column(String(100), nullable=False)
    email: Mapped[str] = Column(EmailType, nullable=False, unique=True)
    token: Mapped[uuid4] = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    create_date: Mapped[datetime] = Column(TIMESTAMP, default=datetime.now())
    modified_date: Mapped[datetime] = Column(TIMESTAMP, default=datetime.now())

