from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from src.db.base import Base


class NotificationModel(Base):

    __tablename__ = "notifications"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )


    title = Column(String(255), nullable=False)

    message = Column(Text, nullable=False)

    status = Column(String(20), nullable=False)


    created_at = Column(
        DateTime,
        server_default=func.now()
    )