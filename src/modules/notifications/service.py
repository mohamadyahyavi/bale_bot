from src.modules.requests.enums import RequestType
from src.modules.requests.enums import RequestStatus
from src.integrations.bale.client import BaleClient as bale

class NotificationService:


    async def notify_new_request(
        self,
        manager_id,
        first_name,
        last_name,
        request_type: RequestType
    ):

        request_type_text = {

            RequestType.LEAVE.value: "مرخصی 🏖️",

            RequestType.REMOTE.value: "دورکاری 🏠",

            RequestType.OVERTIME.value: "اضافه کاری ⏱️",

            RequestType.MISSION.value: "ماموریت 🚗"

        }.get(
            request_type.value,
            request_type.value
        )

        message = (
            "📌 درخواست جدید ثبت شد\n\n"
            f"👤 کارمند: {first_name} {last_name}\n"
            f"📄 نوع درخواست: {request_type_text}"
        )

        return await self.bale.send_message(
            manager_id,
            message
        )



    async def notify_request_result(
        self,
        user_id,
        first_name,
        last_name,
        request_type: RequestType,
        status: RequestStatus
    ):


        request_type_text = {

            RequestType.LEAVE.value: "مرخصی 🏖️",

            RequestType.REMOTE.value: "دورکاری 🏠",

            RequestType.OVERTIME.value: "اضافه کاری ⏱️",

            RequestType.MISSION.value: "ماموریت 🚗"

        }.get(
            request_type.value,
            request_type.value
        )


        status_text = {

            RequestStatus.ACCEPTED.value:
                "تایید شد ✔️",

            RequestStatus.REJECTED.value:
                "رد شد ❌"

        }.get(
            status.value,
            status.value
        )


        message = (
            "📢 وضعیت درخواست شما تغییر کرد\n\n"
            f"👤 کارمند: {first_name} {last_name}\n"
            f"📄 نوع درخواست: {request_type_text}\n"
            f"📊 وضعیت: {status_text}"
        )
    
        return await self.bale.send_message(
            user_id,
            message
        )