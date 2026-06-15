from .entity import NotificationEntity


class NotificationService:

    def __init__(self, repository, bale_client):
        self.repo = repository
        self.bale = bale_client


    async def _send_to_bale(self, user_id, title, message):

        await self.bale.send_message(
            user_id,
            f"{title}\n\n{message}"
        )


    async def notify(
        self,
        user_id,
        title: str,
        message: str,
        send_to_bale: bool = True
    ):

        notification = NotificationEntity(
            user_id=user_id,
            title=title,
            message=message,
            status="SENT" if send_to_bale else "PENDING"
        )

        saved = await self.repo.create(notification)

        try:
            if send_to_bale:
                await self._send_to_bale(user_id, title, message)

        except Exception:
            # در صورت fail شدن ارسال
            saved.status = "FAILED"

        return saved


    # -------------------------
    # BUSINESS METHODS
    # -------------------------

    async def notify_new_request(self, manager_id, first_name, last_name, request_type):

        message = (
            "📌 درخواست جدید ثبت شد\n\n"
            f"👤 کارمند: {first_name} {last_name}\n"
            f"📄 نوع درخواست: {request_type}"
        )

        return await self.notify(
            user_id=manager_id,
            title="New Request",
            message=message
        )


    async def notify_request_result(self, user_id, first_name, last_name, request_type, status):

        status_text = {
            "APPROVED": "تایید شد ✔️",
            "REJECTED": "رد شد ❌"
        }.get(status, status)

        message = (
            "📢 وضعیت درخواست شما تغییر کرد\n\n"
            f"👤 کارمند: {first_name} {last_name}\n"
            f"📄 نوع درخواست: {request_type}\n"
            f"📊 وضعیت: {status_text}"
        )

        return await self.notify(
            user_id=user_id,
            title="Request Update",
            message=message
        )