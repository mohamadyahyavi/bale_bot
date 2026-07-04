from src.modules.users.repository import UserRepository
from src.modules.notifications.service import NotificationService



class WorkEndNotificationJob:

    def __init__(
        self,
        session_factory,
        notification_service: NotificationService
    ):

           self.session_factory = session_factory
           self.notification = notification_service

    async def run(self):    

        async with self.session_factory() as db:

            users = UserRepository(db)
            active_users = await users.get_active_users()

            for user in active_users:
              await self.notification.notify_work_end(
                user.bale_user_id
            )