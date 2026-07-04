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
        manager_bale_id,
        first_name,
        last_name,
        request_type: RequestType
    ):

        message = (
            "📌 درخواست جدید ثبت شد\n\n"
            f"👤 کارمند: {first_name} {last_name}\n"
            f"📄 نوع درخواست: {REQUEST_TYPE_TEXT.get(request_type, request_type.value)}"
        )



        await self.bale.send_message(manager_bale_id, message)

    async def notify_request_result(
        self,
        user_bale_id,
        first_name,
        last_name,
        request_type: RequestType,
        status: RequestStatus,
        reason: str | None = None
    ):

        message = (
            "📢 وضعیت درخواست تغییر کرد\n\n"
            f"👤 کارمند: {first_name} {last_name}\n"
            f"📄 نوع درخواست: {REQUEST_TYPE_TEXT.get(request_type, request_type.value)}\n"
            f"📊 وضعیت: {STATUS_TEXT.get(status, status.value)}"
            
        )

        if status == RequestStatus.REJECTED and reason:
           message += (
            f"\n\n❌ دلیل رد درخواست:\n"
            f"{reason}"
            )


        return await self.bale.send_message(
            user_bale_id,
            message
        )

        #return await self.bale.send_message(user_bale_id, message)
    

    async def notify_missing_hours(self, user_bale_id, missing_hours):

        message = (
            "⚠️ کسری کار امروز\n\n"
            f"⏱ شما {missing_hours} ساعت کسری دارید"
            )

        await self.bale.send_message(user_bale_id, message)


    async def notify_open_timer(self, user_bale_id):

        message = "لظفا تایمر خود را ببندید شما تایمر باز دارید"

        await self.bale.send_message(user_bale_id, message)


    async def notify_no_checkin(self, user_bale_id):

        message = "❌ امروز هیچ ساعت کاری ثبت نکرده‌اید"

        await self.bale.send_message(user_bale_id, message)


    async def notify_daily_report(self, user_bale_id, report):

        message = (
            "📊 گزارش روزانه\n\n"
            f"⏱ کارکرد: {report.worked_hours}\n"
            f"⚠️ کسری: {report.missing_hours}\n"
            f"➕ اضافه‌کاری: {report.overtime_hours}"
        )

        await self.bale.send_message(user_bale_id, message)


    async def notify_weekly_report(self, user_bale_id, report):

        message = (
            "📊 گزارش هفتگی\n\n"
            f"⏱ مجموع کارکرد: {report.worked_hours}\n"
            f"⚠️ کسری: {report.missing_hours}\n"
            f"📁 پروژه‌ها: {len(report.projects)}"
        )

        await self.bale.send_message(user_bale_id, message)


    async def notify_monthly_report(self, user_bale_id, report):

        message = (
            "📊 گزارش ماهانه\n\n"
            f"⏱ مجموع کارکرد: {report.worked_hours}\n"
            f"⚠️ کسری: {report.missing_hours}\n"
            f"➕ اضافه‌کاری: {report.overtime_hours}"
        )

        await self.bale.send_message(user_bale_id, message)  



    async def notify_work_start_reminder(self, user_bale_id: str):

        message = (
            "🌅 یادآوری شروع کار\n\n"
            "لطفاً کار خود را آغاز کرده و تایمر را فعال کنید."
        )

        await self.bale.send_message(user_bale_id, message)


    async def notify_work_end_reminder(self, user_bale_id: str):

        message = (
            "🌙 یادآوری پایان کار\n\n"
            "لطفاً تایمر را متوقف کرده یا ساعات کاری خود را ثبت کنید."
        )

        await self.bale.send_message(user_bale_id, message)  

    async def send_custom(
          self,
          user_bale_id: str,
          message: str
          ):

        return await self.bale.send_message(
        user_bale_id,
        message
        ) 

    async def notify_pending_requests_exists(self, manager_bale_id: str):

        message = (
        "📌 درخواست‌های در انتظار تأیید\n\n"
        "شما درخواست‌های بررسی نشده دارید.\n"
        "لطفاً وارد سیستم شوید و بررسی کنید."
        )

        await self.bale.send_message(manager_bale_id, message) 

    async def notify_leave_limit_reached(
        self,
        user_bale_id: str
    ):

        message = (
        "⚠️ امکان ثبت درخواست مرخصی وجود ندارد\n\n"
        "سقف مجاز مرخصی شما پر شده است.\n"
        )

        await self.bale.send_message(
        user_bale_id,
        message
        )

    async def notify_leave_hours(self,user_bale_id,hours):
          message = (
          f"⚠️  ساعات مجاز مزخصی شما {hours} است\n\n"
          )
          await self.bale.send_message(user_bale_id,message) 


    async def notify_wrong_start_or_end_leave_time(self,user_bale_id):

          message=("به زمان شروع و پایان مرخصی توجه کنید")

          await self.bale.send_message(user_bale_id,message)       
         

    async def notify_worK_start_reminder(self,user_bale_id):

          message-("شروع ساعت کاری خود را در سامانه ثبت کنید")

          await self.bale.send_message(user_bale_id,message)


    async def notify_work_start(self,user_bale_id):

          message=("شروع ساعت کاری خود رو ثبت کنید")

          await self.bale.send_message(user_bale_id,message)


    async def notify_work_end(self,user_bale_id):

          message=("تایم کاری رو به اتمام است لطفا تایمر خود را ببندید")  

          await self.bale.send_message(user_bale_id,message) 

    async def notify_hr_start_job(self,user_bale_id,first_name,last_name):

           text = (
           f"⚠️ {first_name} {last_name} "
           f"امروز هنوز شروع ساعت کاری خود را ثبت نکرده است."

           )  

           await self.bale.send_message(
           user_bale_id,
           text,
           )
          
