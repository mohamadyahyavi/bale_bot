from datetime import datetime

from src.modules.users.entity import User
from src.modules.users.service import UserService
from src.integrations.bale.client import BaleClient


USER_REGISTRATION_SESSIONS = {}


class UserRegistrationHandler:

    def __init__(
        self,
        user_service: UserService,
        bale_client: BaleClient,
    ):
        self.user_service = user_service
        self.bale = bale_client

    async def is_in_flow(
        self,
        bale_user_id: str,
    ):
        return bale_user_id in USER_REGISTRATION_SESSIONS

    async def start_flow(
        self,
        bale_user_id: str,
    ):

        USER_REGISTRATION_SESSIONS[bale_user_id] = {
            "step": "bale_user_id",
            "data": {},
        }

        return await self.bale.send_message(
            bale_user_id,
            "Bale User ID را وارد کنید:"
        )

    async def handle_message(
        self,
        bale_user_id: str,
        message: dict,
    ):

        session = USER_REGISTRATION_SESSIONS.get(
            bale_user_id
        )

        if session is None:

            return await self.bale.send_message(
                bale_user_id,
                "ابتدا گزینه «افزودن کاربر» را انتخاب کنید."
            )

        text = message.get(
            "text",
            ""
        ).strip()

        step = session["step"]

        if step == "bale_user_id":

            session["data"]["bale_user_id"] = text
            session["step"] = "first_name"

            return await self.bale.send_message(
                bale_user_id,
                "نام:"
            )

        elif step == "first_name":

            session["data"]["first_name"] = text
            session["step"] = "last_name"

            return await self.bale.send_message(
                bale_user_id,
                "نام خانوادگی:"
            )

        elif step == "last_name":

            session["data"]["last_name"] = text
            session["step"] = "email"

            return await self.bale.send_message(
                bale_user_id,
                "ایمیل:"
            )

        elif step == "email":

            session["data"]["email"] = text
            session["step"] = "mobile"

            return await self.bale.send_message(
                bale_user_id,
                "شماره موبایل:"
            )

        elif step == "mobile":

            session["data"]["mobile"] = text
            session["step"] = "department_id"

            return await self.bale.send_message(
                bale_user_id,
                "Department UUID را وارد کنید:"
            )

        elif step == "department_id":

            session["data"]["department_id"] = text
            session["step"] = "kimai_user_id"

            return await self.bale.send_message(
                bale_user_id,
                "Kimai User ID:"
            )

        elif step == "kimai_user_id":

            session["data"]["kimai_user_id"] = int(text)
            session["step"] = "contract_start_date"

            return await self.bale.send_message(
                bale_user_id,
                "تاریخ شروع قرارداد (YYYY-MM-DD):"
            )

        elif step == "contract_start_date":

            session["data"]["contract_start_date"] = datetime.strptime(
                text,
                "%Y-%m-%d"
            ).date()

            session["step"] = "contract_end_date"

            return await self.bale.send_message(
                bale_user_id,
                "تاریخ پایان قرارداد (YYYY-MM-DD):"
            )

        elif step == "contract_end_date":

            session["data"]["contract_end_date"] = datetime.strptime(
                text,
                "%Y-%m-%d"
            ).date()

            session["step"] = "access_level"

            return await self.bale.send_message(
                bale_user_id,
                "سطح دسترسی (EMPLOYEE / HR / CEO):"
            )

        elif step == "access_level":

            session["data"]["access_level"] = text.upper()

            data = session["data"]

            user = User(
                id=None,
                bale_user_id=data["bale_user_id"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                mobile=data["mobile"],
                department_id=data["department_id"],
                kimai_user_id=data["kimai_user_id"],
                contract_start_date=data["contract_start_date"],
                contract_end_date=data["contract_end_date"],
                is_active=True,
                total_leave_hours=0,
                access_level=data["access_level"],
            )

            await self.user_service.create_user(
                user
            )

            USER_REGISTRATION_SESSIONS.pop(
                bale_user_id,
                None
            )

            return await self.bale.send_message(
                bale_user_id,
                "✅ کاربر با موفقیت ایجاد شد."
            )