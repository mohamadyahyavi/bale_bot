import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID, JSONB

from sqlalchemy.sql import func

from src.db.base import Base



class RequestModel(Base):

    __tablename__ = "requests"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    manager_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="RESTRICT"
        ),
        nullable=False
    )


    type = Column(
        String(20),
        nullable=False
    )


    status = Column(
        String(20),
        nullable=False,
        default="PENDING"
    )


    data = Column(
        JSONB,
        nullable=False
    )

    message_id = Column(
    String,
    nullable=True
    )

    reject_reason = Column(
        String,
        nullable=True
    )



    created_at = Column(
        DateTime,
        server_default=func.now()
    )


    processed_at = Column(
        DateTime,
        nullable=True
    )