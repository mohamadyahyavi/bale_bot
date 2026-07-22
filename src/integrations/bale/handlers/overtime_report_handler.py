from datetime import datetime

from src.modules.reports.service import OvertimeReportService
from src.modules.users.repository import UserRepository
from src.integrations.bale.client import BaleClient


OVERTIME_REPORT_SESSIONS = {}


class OvertimeReportHandler:

    def __init__(
        self,
        overtime_report_service: OvertimeReportService,
        user_repository: UserRepository,
        bale_client: BaleClient,
        bot
    ):
        self.service = overtime_report_service
        self.user_repository = user_repository
        self.bale = bale_client
        self.bot=bot

    # ===========================
    # FLOW CHECK
    # ===========================

    async def is_in_flow(
        self,
        bale_user_id: str
    ) -> bool:

        return bale_user_id in OVERTIME_REPORT_SESSIONS

    # ===========================
    # START FLOW
    # ===========================

    async def start_flow(
        self,
        bale_user_id: str
    ):

        OVERTIME_REPORT_SESSIONS[bale_user_id] = {
            "step": "title",
            "data": {}
        }

        return await self.bale.send_message(
            bale_user_id,
            "عنوان گزارش اضافه کاری را وارد کنید:"
        )

    # ===========================
    # HANDLE MESSAGE
    # ===========================

    async def show_last_30_days_reports(
        self,
        bale_user_id: str,
    ):

        reports = await self.service.get_last_30_days_reports()

        if not reports:

            return await self.bale.send_message(
                bale_user_id,
                "در ۳۰ روز گذشته هیچ گزارش اضافه کاری ثبت نشده است."
            )

        for report in reports:

            user = await self.user_repository.get_by_id(
                report.user_id
            )

            caption = (
                f"👤 {user.first_name} {user.last_name}\n"
                f"📄 {report.file_name}\n"
                f"📅 {report.created_at.strftime('%Y-%m-%d %H:%M')}"
            )

            await self.bale.send_document(
            chat_id=bale_user_id,
            file_bytes=report.report_file,
            file_name=report.file_name,
            caption=caption,
        )
            
    async def show_team_last_30_days_reports(
        self,
        bale_user_id: str,
    ):

        reports = await self.service.get_team_last_30_days_reports(
            bale_user_id
        )

        if not reports:

            return await self.bale.send_message(
                bale_user_id,
                "در ۳۰ روز گذشته هیچ گزارش اضافه کاری برای اعضای تیم شما ثبت نشده است."
            )

        for report in reports:

            user = await self.user_repository.get_by_id(
                report.user_id
            )

            caption = (
                f"👤 {user.first_name} {user.last_name}\n"
                f"📄 {report.file_name}\n"
                f"📅 {report.created_at.strftime('%Y-%m-%d %H:%M')}"
            )

            await self.bale.send_document(
                chat_id=bale_user_id,
                file_bytes=report.report_file,
                file_name=report.file_name,
                caption=caption,
            )

        return

    async def handle_message(
        self,
        bale_user_id: str,
        message: dict
    ):

        session = OVERTIME_REPORT_SESSIONS.get(
            bale_user_id
        )

        if session is None:

            return await self.bale.send_message(
                bale_user_id,
                "ابتدا گزینه «ارسال گزارش اضافه کاری» را انتخاب کنید."
            )

        step = session["step"]

        # -------------------------
        # STEP 1 : TITLE
        # -------------------------

        if step == "title":

            title = message.get(
                "text",
                ""
            ).strip()

            if not title:

                return await self.bale.send_message(
                    bale_user_id,
                    "نام گزارش نمی‌تواند خالی باشد."
                )

            session["data"]["title"] = title

            session["step"] = "file"

            return await self.bale.send_message(
                bale_user_id,
                "فایل گزارش را ارسال کنید."
            )

        # -------------------------
        # STEP 2 : FILE
        # -------------------------

        if step == "file":

            document = message.get(
                "document"
            )

            if not document:

                return await self.bale.send_message(
                    bale_user_id,
                    "لطفا فایل گزارش را ارسال کنید."
                )

            file_bytes = await self.bot.get_file(
                document["file_id"]
            )


            await self.service.create_report(
            bale_user_id=bale_user_id,
            title=session["data"]["title"],
            report_file=file_bytes,
            )

            OVERTIME_REPORT_SESSIONS.pop(
                bale_user_id,
                None
            )

            return await self.bale.send_message(
                bale_user_id,
                "✅ گزارش اضافه کاری با موفقیت ثبت شد."
            )