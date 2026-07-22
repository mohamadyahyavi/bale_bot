from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.reports.entity import OvertimeReport
from src.modules.reports.model import OvertimeReportModel
from src.modules.users.model import UserModel
from src.modules.departments.model import DepartmentModel


class OvertimeReportRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    def _to_entity(
        self,
        model: OvertimeReportModel
    ) -> OvertimeReport:

        return OvertimeReport(
            id=model.id,
            user_id=model.user_id,
            file_name=model.file_name,
            report_file=model.report_file,
            created_at=model.created_at
        )


    async def create(
        self,
        report: OvertimeReport
    ) -> OvertimeReport:

        model = OvertimeReportModel(
            user_id=report.user_id,
            file_name=report.file_name,
            report_file=report.report_file
        )

        self.session.add(model)

        await self.session.commit()

        await self.session.refresh(model)

        return self._to_entity(model)


    async def get_by_id(
        self,
        report_id: UUID
    ):

        stmt = select(
            OvertimeReportModel
        ).where(
            OvertimeReportModel.id == report_id
        )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._to_entity(model)
    
    async def get_last_30_days_reports(self):

        from_date = datetime.now() - timedelta(days=30)

        stmt = (
        select(OvertimeReportModel)
        .where(
            OvertimeReportModel.created_at >= from_date
        )
        .order_by(
            OvertimeReportModel.created_at.desc()
        )
    )

        result = await self.session.execute(stmt)

        reports = result.scalars().all()

        return [
        self._to_entity(report)
        for report in reports
    ]

    async def get_last_30_days_team_reports(
    self,
    manager_user_id: UUID,
):

        from_date = datetime.now() - timedelta(days=30)

        stmt = (
        select(OvertimeReportModel)
        .join(
            UserModel,
            OvertimeReportModel.user_id == UserModel.id,
        )
        .join(
            DepartmentModel,
            UserModel.department_id == DepartmentModel.id,
        )
        .where(
            DepartmentModel.manager_user_id == manager_user_id,
            OvertimeReportModel.created_at >= from_date,
        )
        .order_by(
            OvertimeReportModel.created_at.desc()
        )
    )

        result = await self.session.execute(stmt)
 
        reports = result.scalars().all()

        return [
        self._to_entity(report)
        for report in reports
    ]


    async def get_by_user(
        self,
        user_id: UUID
    ):

        stmt = (
            select(OvertimeReportModel)
            .where(
                OvertimeReportModel.user_id == user_id
            )
            .order_by(
                OvertimeReportModel.created_at.desc()
            )
        )

        result = await self.session.execute(stmt)

        models = result.scalars().all()

        return [
            self._to_entity(model)
            for model in models
        ]