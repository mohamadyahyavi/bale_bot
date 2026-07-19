from datetime import datetime, date, timedelta

from src.integrations.bale.keyboards import (
    projects_keyboard,
    activities_keyboard
)
from .time_entry_form import TimeEntryForm
from src.integrations.bale.client import BaleClient
from src.integrations.kimai.service import KimaiService
from src.modules.users.repository import UserRepository
from src.modules.logs.service import LogService
from src.modules.logs.enums import LogAction


TIME_ENTRY_SESSIONS = {}


class TimeEntryHandler:


    def __init__(
        self,
        kimai_service:KimaiService,
        user_repositpry:UserRepository,
        bale_client:BaleClient,
        log_service:LogService
    ):

        self.kimai_service = kimai_service
        self.user_repository=user_repositpry
        self.bale = bale_client
        self.log_service = log_service
        self.form = TimeEntryForm()

    # =========================
    # START FLOW
    # =========================

    async def start_flow(
        self,
        bale_user_id: str
    ):

        projects = await self.kimai_service.get_all_projects()
        user = await self.user_repository.get_by_bale_id(bale_user_id)

        if not projects:

            return await self.bale.send_message(
                bale_user_id,
                "❌ هیچ پروژه‌ای برای انتخاب وجود ندارد."
            )

        TIME_ENTRY_SESSIONS[bale_user_id] = {

            "step": "project",

            "data": { "kimai_user_id":user.kimai_user_id}

        }
        await self.bale.send_message(
            bale_user_id,
            "پروژه مورد نظر را انتخاب کنید: لطفا ",
            keyboard=projects_keyboard(projects)
        )

    # =========================
    # CHECK FLOW
    # =========================
    async def is_in_flow(
        self,
        bale_user_id
    ):

        return bale_user_id in TIME_ENTRY_SESSIONS

    # =========================
    # HANDLE MESSAGE
    # =========================
    async def handle_message(
        self,
        bale_user_id,
        text
    ):


        session = TIME_ENTRY_SESSIONS.get(
            bale_user_id
        )

        if not session:

            return

        step = session["step"]

        # -------------------------
        # PROJECT
        # -------------------------

        if step == "project":


            projects = await self.kimai_service.get_all_projects()


            project = next(
                (
                    p
                    for p in projects
                    if p["name"] == text
                ),
                None
            )


            if not project:

                return await self.bale.send_message(
                    bale_user_id,
                    "❌ پروژه نامعتبر است."
                )


            session["data"]["project"] = project["id"]


            activities = await self.kimai_service.get_all_activities()


            if not activities:

                return await self.bale.send_message(
                    bale_user_id,
                    "❌ هیچ فعالیتی وجود ندارد."
                )


            session["step"] = "activity"


            return await self.bale.send_message(
                bale_user_id,
                "فعالیت را انتخاب کنید:",
                keyboard=activities_keyboard(
                    activities
                )
            )

        # -------------------------
        # ACTIVITY
        # -------------------------

        if step == "activity":


            activities = await self.kimai_service.get_all_activities()


            activity = next(
                (
                    a
                    for a in activities
                    if a["name"] == text
                ),
                None
            )


            if not activity:

                return await self.bale.send_message(
                    bale_user_id,
                    "❌ فعالیت نامعتبر است."
                )

            session["data"]["activity"] = activity["id"]


            session["step"] = "begin"


            return await self.bale.send_message(
                bale_user_id,
                "⏰ زمان شروع را وارد کنید.\nمثال: 09:30"
            )



        # -------------------------
        # BEGIN
        # -------------------------


        if step == "begin":


            if not self.validate_time(text):

                return await self.bale.send_message(
                    bale_user_id,
                    "❌ فرمت ساعت اشتباه است.\nمثال: 09:30"
                )


            session["data"]["begin"] = text


            session["step"] = "end"


            return await self.bale.send_message(
                bale_user_id,
                "⏰ زمان پایان را وارد کنید.\nمثال: 11:30"
            )



        # -------------------------
        # END
        # -------------------------


        if step == "end":


            if not self.validate_time(text):

                return await self.bale.send_message(
                    bale_user_id,
                    "❌ فرمت ساعت اشتباه است."
                )



            begin = session["data"]["begin"]


            if not self.validate_duration(
                begin,
                text
            ):

                return await self.bale.send_message(
                    bale_user_id,
                    "❌ بازه زمانی نباید بیشتر از ۳ ساعت باشد."
                )


            session["data"]["end"] = text


            session["step"] = "description"



            return await self.bale.send_message(
                bale_user_id,
                "📝 توضیحات کار را وارد کنید:"
            )



        # -------------------------
        # DESCRIPTION
        # -------------------------


        if step == "description":


            session["data"]["description"] = text



            data = session["data"]


            today = date.today().strftime(
                "%Y-%m-%d"
            )


            begin_datetime = (
                f"{today}T{data['begin']}:00"
            )

            end_datetime = (
                f"{today}T{data['end']}:00"
            )
            user = await self.user_repository.get_by_bale_id(bale_user_id)


            try:


                await self.kimai_service.create_timesheet(

                    begin=begin_datetime,

                    end=end_datetime,

                    project=data["project"],

                    activity=data["activity"],

                    description=data["description"],

                    kimai_user_id=session["data"]["kimai_user_id"]

                )

                await self.log_service.log_success(
                user_id=user.id,
                action=LogAction.CREATE_TIMESHEET,
                description=(
                f"ثبت ساعت کاری | "
                f"شروع: {begin_datetime} | "
                f"پایان: {end_datetime} | "
                f"پروژه: {data['project']} | "
                f"فعالیت: {data['activity']}"
            )
        )


                del TIME_ENTRY_SESSIONS[bale_user_id]

                return await self.bale.send_message(
                    bale_user_id,
                    "✅ زمان کاری با موفقیت ثبت شد."
                )


            except Exception as e:

                await self.log_service.log_failed(
                user_id=user.id,
                action=LogAction.CREATE_TIMESHEET,
                description=(
                f"ثبت ساعت ناموفق | "
                f"شروع: {begin_datetime} | "
                f"پایان: {end_datetime} | "
                f"خطا: {str(e)}"
            )
        )


                return await self.bale.send_message(
                    bale_user_id,
                    f"❌ خطا در ثبت زمان:\n{str(e)}"
                )
    # =========================
    # VALIDATIONS
    # =========================
    def validate_time(
        self,
        value
    ):

        try:

            datetime.strptime(
                value,
                "%H:%M"
            )

            return True

        except:

            return False

    def validate_duration(
        self,
        begin,
        end
    ):

        start = datetime.strptime(
            begin,
            "%H:%M"
        )

        finish = datetime.strptime(
            end,
            "%H:%M"
        )

        if finish <= start:

            return False

        diff = finish - start

        return diff <= timedelta(
            hours=3
        )