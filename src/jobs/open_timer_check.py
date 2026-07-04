from src.modules.users.repository import UserRepository
from src.integrations.kimai.service import KimaiService
from src.modules.notifications.service import NotificationService


class OpenTimerCheckJob:

    def __init__(self, session_factory, kimai_service, notification_service):

        self.session_factory=session_factory
        self.kimai = kimai_service
        self.notification = notification_service


    async def run(self):

          async with self.session_factory() as db:

            user_repo = UserRepository(db)
            #hr_user= await user_repo.get_hr_user()
            active_users = await user_repo.get_active_users()

            for user in active_users:

                if user.kimai_user_id is None:
                    continue

                open_timesheets = await self.kimai.get_open_timesheets(
                    user.kimai_user_id
                )

                if open_timesheets:
                    await self.notification.notify_open_timer(
                        user.bale_user_id
                    )