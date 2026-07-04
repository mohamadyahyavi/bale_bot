from src.modules.requests.repository import RequestRepository
from src.modules.notifications.service import NotificationService
from src.modules.users.repository import UserRepository


class PendingRequestsJob:

    def __init__(self,session_factory, notification_service:NotificationService):
        self.session_factory=session_factory
        self.notification = notification_service

    async def run(self):

        async with self.session_factory() as db:

            print("Request pending")

            request_repo = RequestRepository(db)
            user_repo = UserRepository(db)

            manager_bale_ids = await request_repo.get_managers_with_pending_requests()  # یا manager واقعی

            for manager_bale_id in manager_bale_ids:

                await self.notification.notify_pending_requests_exists(
                manager_bale_id
                )