from src.modules.requests.enums import RequestType, RequestStatus
from src.integrations.bale.client import BaleClient



REQUEST_TYPE_TEXT = {
    RequestType.LEAVE: "مرخصی 🏖️",
    RequestType.REMOTE: "دورکاری 🏠",
    RequestType.OVERTIME: "اضافه کاری ⏱️",
    RequestType.MISSION: "ماموریت 🚗",
}

STATUS_TEXT = {
    RequestStatus.ACCEPTED: "تایید شد ✔️",
    RequestStatus.REJECTED: "رد شد ❌",
}


class NotificationService:

    def __init__(self, bale_client: BaleClient):
        self.bale = bale_client
        

    async def notify_new_request(
        self,
        manager_id,
        first_name,
        last_name,
        request_type: RequestType
    ):

        message = (
            "📌 درخواست جدید ثبت شد\n\n"
            f"👤 کارمند: {first_name} {last_name}\n"
            f"📄 نوع درخواست: {REQUEST_TYPE_TEXT.get(request_type, request_type.value)}"
        )



        await self.bale.send_message(manager_id, message)

    async def notify_request_result(
        self,
        user_id,
        first_name,
        last_name,
        request_type: RequestType,
        status: RequestStatus
    ):

        message = (
            "📢 وضعیت درخواست شما تغییر کرد\n\n"
            f"👤 کارمند: {first_name} {last_name}\n"
            f"📄 نوع درخواست: {REQUEST_TYPE_TEXT.get(request_type, request_type.value)}\n"
            f"📊 وضعیت: {STATUS_TEXT.get(status, status.value)}"
        )

        return await self.bale.send_message(user_id, message)