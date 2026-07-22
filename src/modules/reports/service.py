from uuid import UUID

from src.modules.reports.entity import OvertimeReport
from src.modules.reports.repository import (
    OvertimeReportRepository,
)
from src.modules.users.repository import UserRepository
from src.modules.users.entity import User

class OvertimeReportService:

    def __init__(
        self,
        repository: OvertimeReportRepository,
        user_repository: UserRepository,
    ):
        self.repository = repository
        self.user_repository = user_repository

    async def create_report(
        self,
        bale_user_id: str,
        title: str,
        report_file: bytes,
    ):

        user = await self.user_repository.get_by_bale_id(
            bale_user_id
        )

        if not user:
            raise Exception("User not found")

        report = OvertimeReport(
            id=None,
            user_id=user.id,
            file_name=title,
            report_file=report_file,
        )

        return await self.repository.create(report)


    async def get_report(
        self,
        report_id: UUID,
    ):

        return await self.repository.get_by_id(
            report_id
        )
    
    async def get_last_30_days_reports(self):

        return await self.repository.get_last_30_days_reports()


    async def get_user_reports(
        self,
        user_id: UUID,
    ):

        return await self.repository.get_by_user(
            user_id
        )
    
    async def get_team_last_30_days_reports(self,bale_user_id):

        manager = await self.user_repository.get_by_bale_id(
            bale_user_id
        )

        if manager is None:
            raise Exception("Manager not found")

        return await self.repository.get_last_30_days_team_reports(
            manager.id
        )