from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class NotificationEntity:

    user_id: UUID  # receiver

    title: str
    message: str

    status: str = "PENDING"

    id: UUID | None = None
    created_at: datetime | None = None