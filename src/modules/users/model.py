from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from src.db.base import Base


class UserModel(Base):

    __tablename__ = "users"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    bale_user_id = Column(String(100), unique=True, nullable=False)

    first_name = Column(String(100), nullable=False)

    last_name = Column(String(100), nullable=False)

    kimai_user_id = Column(Integer, unique=True, nullable=False)

    department_id = Column(
        UUID(as_uuid=True),
        ForeignKey("departments.id"),
        nullable=False
    )

    is_active = Column(Boolean, default=True, nullable=False)

    email = Column(String(255), nullable=True)

    mobile = Column(String(20), nullable=True)

    contract_start_date = Column(Date, nullable=True)

    contract_end_date = Column(Date, nullable=True)

    total_leave_hours = Column(Integer, default=0, nullable=False)

    access_level = Column(String(20), default="EMPLOYEE", nullable=False)


    # relationship (برای اینکه manager و department قابل دسترسی باشد)
    department = relationship(
        "DepartmentModel",
        back_populates="users",
        foreign_keys=[department_id]
    )