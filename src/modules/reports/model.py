import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, DateTime, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID

from src.db.base import Base


class OvertimeReportModel(Base):

    __tablename__ = "overtime_reports"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    file_name = Column(
        String,
        nullable=False
    )

    report_file = Column(
        LargeBinary,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )