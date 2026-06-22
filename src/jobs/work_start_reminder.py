from src.modules.users.repository import UserRepository
from src.modules.reports.service import ReportService
from src.modules.notifications.service import NotificationService


class WorkStartReminderJob:

    def __init__(
        self,
        user_repo: UserRepository,
        report_service: ReportService,
        notification_service: NotificationService
    ):

        self.users = user_repo
        self.report = report_service
        self.notification = notification_service


    async def run(self):

        users = await self.users.get_active_users()


        for user in users:


            today_status = await self.report.daily(user)


            # اگر امروز هنوز کاری ثبت نکرده
            if today_status.worked_hours == 0:


                await self.notification.notify_work_start_reminder(
                    user.bale_user_id
                )