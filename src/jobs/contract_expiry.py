from datetime import date, timedelta

from src.modules.users.repository import UserRepository
from src.modules.notifications.service import NotificationService


class ContractExpiryJob:


    def __init__(
        self,
        session_factory,
        notification_service: NotificationService
    ):

        self.session_factory = session_factory
        self.notification = notification_service



    async def run(self):


      print("🔥 CONTRACT EXPIRY RUNNING")
      async with self.session_factory() as db:

            users = UserRepository(db)

            today = date.today()

            target_date = today + timedelta(days=5)


            employees = await users.get_users_with_contract_expiry(today,
            target_date
        )

            if not employees:
               return

            hr = await users.get_hr_user()

            message = (
                "⚠️ هشدار پایان قرارداد\n\n"
                "قرارداد افراد زیر ۵ روز دیگر به پایان می‌رسد:\n\n"
            )


            for user in employees:

                message += (
                    f"👤 {user.first_name} {user.last_name}\n"
                    f"📅 پایان قرارداد: {user.contract_end_date}\n\n"
                )


            await self.notification.send_custom(
                hr.bale_user_id,
                message
            )