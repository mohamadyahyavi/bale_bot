from src.modules.users.repository import UserRepository
from src.modules.reports.service import ReportService
from src.modules.notifications.service import NotificationService


class OpenTimerCheckJob:

    def __init__(self, user_repo, report_service, notification_service):

        self.users = user_repo
        self.report = report_service
        self.notification = notification_service


    async def run(self):

        users = await self.users.get_active_users()

        for user in users:

            has_open = await self.report.has_open_timer(user)

            if has_open:

                await self.notification.notify_open_timer(
                    user.bale_user_id
                )