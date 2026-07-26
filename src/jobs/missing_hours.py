from datetime import date

from src.modules.users.repository import UserRepository
from src.integrations.kimai.service import KimaiService
from src.modules.notifications.service import NotificationService


class MissingHoursJob:

    REQUIRED_MINUTES = 7 * 60

    def __init__(self, session_factory,
                 kimai_service: KimaiService,
                 notification_service: NotificationService):

        self.session_factory = session_factory
        self.kimai = kimai_service
        self.notification = notification_service


    async def run(self):

      async with self.session_factory() as db:

        user_repo = UserRepository(db)

        users = await user_repo.get_active_users()

        for user in users:

            worked = await self.kimai.get_today_worked_duration(
                user.kimai_user_id
            )

            hours, minutes = map(int, worked.split(":"))
            worked_minutes = hours * 60 + minutes

            if worked_minutes < self.REQUIRED_MINUTES:

                missing_minutes = self.REQUIRED_MINUTES - worked_minutes

                h = missing_minutes // 60
                m = missing_minutes % 60

                message = (
                    "⏰ یادآوری پایان روز\n\n"
                    "کارکرد امروز شما هنوز کامل نشده است.\n"
                    f"⏳ کسری کار: {h} ساعت و {m} دقیقه\n\n"
                    "لطفاً در صورت وجود تایم ثبت‌نشده، آن را در Kimai ثبت کنید."
                )

                await self.notification.notify_missing_hours(
                    user.bale_user_id,
                    message,
                )