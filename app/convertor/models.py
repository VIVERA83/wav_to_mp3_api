"""Модели сервиса Convertor."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, Column, String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from store.database.database import Base


class Mp3Model(Base):
    """Модель, Mp3."""
    __tablename__ = "mp3"  # noqa

    id: Mapped[uuid4] = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    mp3: Mapped[bytes] = Column(LargeBinary)
    file_name: Mapped[str] = Column(String(150))
    create_date: Mapped[datetime] = Column(TIMESTAMP, default=datetime.now())

    user_id: Mapped[uuid4] = Column(UUID(as_uuid=True), default=uuid4)
