from datetime import date
from calendar import monthrange

from src.integrations.kimai.service import KimaiService
from src.modules.reports.calculator import ReportCalculator
from src.modules.reports.builder import ReportBuilder


class ReportService:

    def __init__(
        self,
        #kimai_service: KimaiService,
        calculator: ReportCalculator,
        builder: ReportBuilder
    ):
        #self.kimai = kimai_service
        self.calc = calculator
        self.builder = builder

    # =========================
    # DAILY REPORT
    # =========================
    async def daily(self, user, report_date: date):

        logs = await self.kimai.get_user_worklogs(
            user.kimai_user_id,
            report_date,
            report_date
        )

        worked = self.calc.worked_hours(logs)
        missing = self.calc.missing_hours(worked)
        overtime = self.calc.overtime_hours(worked)

        open_timer = await self.kimai.has_open_timer(
            user.kimai_user_id
        )

        return self.builder.build_daily(
            user=user,
            logs=logs,
            worked=worked,
            missing=missing,
            overtime=overtime,
            open_timer=open_timer
        )

    # =========================
    # WEEKLY REPORT
    # =========================
    async def weekly(self, user, start_date, end_date):

        logs = await self.kimai.get_user_worklogs(
            user.kimai_user_id,
            start_date,
            end_date
        )

        worked = self.calc.worked_hours(logs)

        return self.builder.build_weekly(
            user=user,
            logs=logs,
            worked=worked,
            missing=self.calc.missing_hours(worked),
            overtime=self.calc.overtime_hours(worked)
        )

    # =========================
    # MONTHLY REPORT
    # =========================
    async def monthly(self, user, month: int, year: int):

        last_day = monthrange(year, month)[1]

        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{last_day}"

        logs = await self.kimai.get_user_worklogs(
            user.kimai_user_id,
            start_date,
            end_date
        )

        worked = self.calc.worked_hours(logs)

        return self.builder.build_monthly(
            user=user,
            logs=logs,
            worked=worked,
            missing=self.calc.missing_hours(worked),
            overtime=self.calc.overtime_hours(worked)
        )