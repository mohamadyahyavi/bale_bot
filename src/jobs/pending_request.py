from src.modules.requests.repository import RequestRepository
from src.modules.notifications.service import NotificationService
from src.modules.users.repository import UserRepository


class PendingRequestsJob:

    def __init__(self, request_repo:RequestRepository, user_repo:UserRepository, notification_service:NotificationService):
        self.requests = request_repo
        self.users = user_repo
        self.notification = notification_service

    async def run(self):

        manager_ids = await self.requests.get_managers_with_pending_requests()  # یا manager واقعی

        if not manager_ids:
            return

        for manager_id in manager_ids:

            manager = await self.users.get_by_id(manager_id)

            if not manager:
                continue

            await self.notification.notify_pending_requests_exists(
                manager.bale_user_id
            )