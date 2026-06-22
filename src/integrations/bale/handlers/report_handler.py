from datetime import date, timedelta

from src.modules.users.service import UserService
from src.modules.reports.service import ReportService
from src.integrations.bale.client import BaleClient


class ReportHandler:

    def __init__(
        self,
        user_service: UserService,
        report_service: ReportService,
        bale_client: BaleClient
    ):
        self.user_service = user_service
        self.report_service = report_service
        self.bale = bale_client

    # =========================
    # MY REPORTS
    # =========================
    async def show_my_reports(self, user_id: str):

        user = await self.user_service.get_by_id(user_id)

        today = date.today()

        report = await self.report_service.daily(user, today)

        message = (
            "📊 گزارش روزانه شما\n\n"
            f"⏱ ساعات کارکرد: {report.worked_hours}\n"
            f"⚠️ کسری: {report.missing_hours}\n"
            f"➕ اضافه‌کاری: {report.overtime_hours}"
        )

        await self.bale.send_message(user.bale_user_id, message)

    # =========================
    # TEAM REPORTS (DAILY)
    # =========================
    async def show_team_reports(self, user_id: str):

        users = await self.user_service.get_team_members(user_id)

        today = date.today()

        message = "👥 گزارش تیم (روزانه)\n\n"

        for user in users:

            report = await self.report_service.daily(user, today)

            message += (
                f"👤 {user.first_name} {user.last_name}\n"
                f"⏱ {report.worked_hours}h | "
                f"⚠️ {report.missing_hours}h | "
                f"➕ {report.overtime_hours}h\n\n"
            )

        await self.bale.send_message(
            chat_id=user_service.get_by_id(user_id).bale_user_id,
            text=message
        )

    # =========================
    # ALL REPORTS (ADMIN)
    # =========================
    async def show_all_reports(self, user_id: str):

        users = await self.user_service.get_active_users()

        today = date.today()

        message = "🏢 گزارش کل سازمان\n\n"

        for user in users:

            report = await self.report_service.daily(user, today)

            message += (
                f"👤 {user.first_name} {user.last_name}\n"
                f"⏱ {report.worked_hours}h | "
                f"⚠️ {report.missing_hours}h | "
                f"➕ {report.overtime_hours}h\n\n"
            )

        await self.bale.send_message(
            chat_id=user_id,
            text=message
        )

    # =========================
    # WEEKLY REPORT (USER)
    # =========================
    async def show_my_weekly_report(self, user_id: str):

        user = await self.user_service.get_by_id(user_id)

        today = date.today()
        start = today - timedelta(days=7)

        report = await self.report_service.weekly(user, start, today)

        message = (
            "📅 گزارش هفتگی شما\n\n"
            f"⏱ مجموع: {report['worked_hours']}\n"
            f"⚠️ کسری: {report['missing_hours']}\n"
            f"➕ اضافه‌کاری: {report['overtime_hours']}\n"
        )

        await self.bale.send_message(user.bale_user_id, message)

    # =========================
    # MONTHLY REPORT (USER)
    # =========================
    async def show_my_monthly_report(self, user_id: str):

        user = await self.user_service.get_by_id(user_id)

        today = date.today()

        report = await self.report_service.monthly(
            user,
            today.month,
            today.year
        )

        message = (
            "📆 گزارش ماهانه شما\n\n"
            f"⏱ مجموع: {report['worked_hours']}\n"
            f"⚠️ کسری: {report['missing_hours']}\n"
            f"➕ اضافه‌کاری: {report['overtime_hours']}\n"
        )

        await self.bale.send_message(user.bale_user_id, message)