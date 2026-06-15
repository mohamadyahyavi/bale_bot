from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from src.db.base import Base


class DepartmentModel(Base):

    __tablename__ = "departments"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(
        String(100),
        nullable=False
    )

    manager_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )


    # relationships
    users = relationship(
        "UserModel",
        back_populates="department"
    )

    manager = relationship(
        "UserModel",
        foreign_keys=[manager_user_id],
        uselist=False
    )