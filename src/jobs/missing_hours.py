from datetime import date

from src.modules.users.repository import UserRepository
from src.modules.reports.service import ReportService
from src.modules.notifications.service import NotificationService


class MissingHoursJob:

    def __init__(self, user_repo: UserRepository,
                 report_service: ReportService,
                 notification_service: NotificationService):

        self.users = user_repo
        self.report = report_service
        self.notification = notification_service


    async def run(self):

        users = await self.users.get_active_users()

        for user in users:

            report = await self.report.daily(user, date.today())

            if report.missing_hours > 0:

                await self.notification.notify_missing_hours(
                    user.bale_user_id,
                    report.missing_hours
                )