from dataclasses import dataclass

from uuid import UUID

from datetime import datetime



@dataclass
class RequestEntity:


    user_id: UUID

    manager_id: UUID

    type: str

    status: str

    data: dict

    id: UUID | None = None

    created_at: datetime | None = None

    processed_at: datetime | None = None