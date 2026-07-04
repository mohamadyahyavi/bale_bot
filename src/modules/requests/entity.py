from dataclasses import dataclass

from uuid import UUID

from datetime import datetime
from src.modules.requests.enums import RequestType, RequestStatus




@dataclass
class RequestEntity:


    user_id: UUID

    manager_id: UUID

    type: RequestType

    status:RequestStatus 

    data: dict

    message_id: str | None = None

    reject_reason: str | None = None

    id: UUID | None = None

    created_at: datetime | None = None

    processed_at: datetime | None = None