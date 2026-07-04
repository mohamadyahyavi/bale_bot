from src.integrations.kimai.service import KimaiService
from src.modules.notifications.service import NotificationService
from src.modules.users.repository import UserRepository


class WorkStartReminderJob:

    def __init__(
        self,
        session_factory,
        kimai_service: KimaiService,
        notification_service: NotificationService,
    ):
        self.session_factory=session_factory
        self.kimai = kimai_service
        self.notification = notification_service

    async def run(self):
        async with self.session_factory() as db:

            user_repo = UserRepository(db)
            hr_user= await user_repo.get_hr_user() 

            active_users = await user_repo.get_active_users()

            for user in active_users:

            # اگر برای کاربر kimai_id ثبت نشده باشد
               if user.kimai_user_id is None:
                  continue

            # اگر امروز هنوز هیچ تایمی ثبت نکرده باشد
               if not await self.kimai.has_work_started_today(
                  user.kimai_user_id,
                  ):
                  await self.notification.notify_work_start_reminder(
                    user.bale_user_id,
                  )
                  
                  await self.notification.notify_hr_start_job(hr_user.bale_user_id,user.first_name,user.last_name)