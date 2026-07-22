from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class OvertimeReport:

    id: UUID | None

    user_id: UUID

    file_name: str

    report_file: bytes

    created_at: datetime | None = None