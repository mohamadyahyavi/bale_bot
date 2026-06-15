from dataclasses import dataclass
from uuid import UUID


@dataclass
class Department:
    

    name: str

    manager_user_id: UUID

    id: UUID | None=None