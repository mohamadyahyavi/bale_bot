from pydantic import BaseModel
from typing import List
from datetime import date


class ProjectReport(BaseModel):
    project: str
    hours: float


class ReportSchema(BaseModel):

    user_id: str

    report_date: date

    worked_hours: float
    required_hours: float

    missing_hours: float
    overtime_hours: float

    has_open_timer: bool

    projects: List[ProjectReport]