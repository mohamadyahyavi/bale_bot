class NotificationTemplates:


    @staticmethod
    def new_request(first_name: str, last_name: str, request_type: str):

        return (
            "📌 درخواست جدید ثبت شد\n\n"
            f"👤 کارمند: {first_name} {last_name}\n"
            f"📄 نوع درخواست: {request_type}\n\n"
            "لطفاً بررسی کنید."
        )


    @staticmethod
    def request_result(first_name: str, last_name: str, request_type: str, status: str):

        status_fa = {
            "APPROVED": "تایید شد ✔️",
            "REJECTED": "رد شد ❌"
        }.get(status, status)


        return (
            "📢 وضعیت درخواست شما تغییر کرد\n\n"
            f"👤 کارمند: {first_name} {last_name}\n"
            f"📄 نوع درخواست: {request_type}\n"
            f"📊 وضعیت: {status_fa}"
        )