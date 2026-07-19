from datetime import datetime
import uuid

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
)

from sqlalchemy.dialects.postgresql import UUID
from src.db.base import Base

class OperationLog(Base):

    __tablename__ = "operation_logs"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


    user_id = Column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
    )


    action = Column(
        String(100),
        nullable=False,
        index=True,
    )


    result = Column(
        String(50),
        nullable=False,
    )


    description = Column(
        Text,
        nullable=True,
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )