from src.integrations.bale.keyboards import request_types_keyboard,request_action_keyboard,leave_types_keyboard
from src.modules.requests.enums import RequestType,RequestStatus
from src.integrations.bale.client import BaleClient
from .request_form_engine import RequestFormEngine
from src.modules.requests.service import RequestService
from src.modules.users.repository import UserRepository
from src.integrations.bale.calendar_keyboard import leave_calendar_keyboard
from datetime import datetime

REQUEST_SESSIONS = {}
class RequestHandler:

    def __init__(
        self,
        request_service: RequestService,
        user_repository:UserRepository,
        bale_client: BaleClient
    ):
        self.request_service = request_service
        self.user_repository=user_repository
        self.bale = bale_client
        self.engine = RequestFormEngine()
        print("REQUEST_HANDLER CREATED", id(self))
        print("SESSION DICT =", id(REQUEST_SESSIONS))

        # session storage (later Redis)
        

    # =========================
    # FLOW CHECK
    # =========================
    async def is_in_flow(self, bale_user_id: str) -> bool:
        return bale_user_id in REQUEST_SESSIONS

    # =========================
    # START FLOW
    # =========================
    async def start_flow(self, bale_user_id: str):

        print("START FLOW")

        REQUEST_SESSIONS[bale_user_id] = {
            "type": None,
            "step": None,
            "data": {}
        }

        print("AFTER START =", REQUEST_SESSIONS)

        print("START FLOW SESSION =", REQUEST_SESSIONS)
        print("START FLOW ID =", id(REQUEST_SESSIONS))

        return await self.bale.send_message(
            bale_user_id,
            "Select request type:",
            keyboard=request_types_keyboard()
        )

    # =========================
    # MAIN HANDLER
    # =========================
    async def handle_message(self, bale_user_id: str, message: dict):

        session = REQUEST_SESSIONS.get(bale_user_id)

        print("HANDLE_MESSAGE")
        print("DICT =", REQUEST_SESSIONS)

        if not session:
            return await self.bale.send_message(
                bale_user_id,
                "Please start request flow first (/create_request)"
            )
        
        text = message.get(
            "text",
            ""
        )

        # =========================
        # STEP 1: TYPE SELECTION
        # =========================
        if session["type"] is None:

            valid_types = [
                RequestType.LEAVE.value,
                RequestType.REMOTE.value,
                RequestType.OVERTIME.value,
                RequestType.MISSION.value
            ]

            if text not in valid_types:
                return await self.bale.send_message(
                    bale_user_id,
                    "Invalid request type"
                )

            session["type"] = RequestType(text)
            session["step"] = self.engine.get_first_step(text)
            print("HANDLE MESSAGE SESSION =", REQUEST_SESSIONS)
            print("HANDLE MESSAGE ID =", id(REQUEST_SESSIONS))
            print("TYPE =", session["type"])
            print("FIRST STEP =", session["step"])

            return await self._ask_next(bale_user_id)

        # =========================
        # STEP 2+: FORM INPUT
        # =========================
        current_step = session["step"]

        if current_step == "medical_document":


            document = message.get(
                "document"
            )

            if not document:

                return await self.bale.send_message(
                    bale_user_id,
                    "❌ Please send your medical document."
                )


            session["data"]["medical_document"] = {

                "file_id": document.get(
                    "file_id"
                ),

                "file_name": document.get(
                    "file_name"
                )
            }


            next_step = None



        else:


            # =========================
            # VALIDATION
            # =========================

            if not self.engine.validate(
                current_step,
                text
            ):


                if current_step in [
                    "start_date",
                    "end_date",
                    "date"
                ]:

                    return await self.bale.send_message(
                        bale_user_id,
                        "❌ Invalid datetime format.\n\n"
                        "Please use this format:\n"
                        "2026-06-30 16:00:00"
                    )

                if current_step in [
                  "start_time",
                  "end_time"
                ]:
                    return await self.bale.send_message(
                    bale_user_id,
                    "❌ Invalid time format.\n\n"
                    "Please use this format:\n"
                    "09:30"
                    )

                if current_step == "leave_type":

                    return await self.bale.send_message(
                        bale_user_id,
                        "❌ Leave type must be DAILY / HOURLY / SICK."
                    )



                if current_step == "hours":

                    return await self.bale.send_message(
                        bale_user_id,
                        "❌ Hours must be a number."
                    )



                return await self.bale.send_message(
                    bale_user_id,
                    f"Invalid value for {current_step}"
                )



            # =========================
            # SAVE ANSWER
            # =========================

            if current_step == "leave_type":

              leave_type = text.strip().upper()

              session["data"]["leave_type"] = leave_type

              if leave_type == "HOURLY":
                 session["step"] = "date"

              else:
                session["step"] = "start_date"

              return await self._ask_next(bale_user_id)

            else:

               session["data"][current_step] = text



            # =========================
            # CHECK SICK LEAVE
            # =========================

            leave_type = session["data"].get("leave_type")


            if leave_type == "HOURLY":

               if current_step == "date":
                  next_step = "start_time"

               elif current_step == "start_time":
                    next_step = "end_time"

               elif current_step == "end_time":
                    next_step = "reason"

               elif current_step == "reason":
                    next_step = None

               else:
                 next_step = None


            elif leave_type == "DAILY":

              if current_step == "start_date":
                next_step = "end_date"

              elif current_step == "end_date":
                next_step = "reason"

              elif current_step == "reason":
                next_step = None

              else:
                next_step = None


            elif leave_type == "SICK":

              if current_step == "start_date":
                 next_step = "end_date"

              elif current_step == "end_date":
                 next_step = "reason"

              elif current_step == "reason":
                 next_step = "medical_document"

              elif current_step == "medical_document":
                   next_step = None

              else:
                next_step = None


            else:

              next_step = self.engine.get_next_step(
              session["type"],
              current_step
              )



        # =========================
        # FINISH FLOW
        # =========================

        if next_step is None:


            await self.request_service.create_request(
                bale_user_id=bale_user_id,
                request_type=session["type"],
                body=session["data"]
            )

            print("POP SESSION")
            print(REQUEST_SESSIONS)
            REQUEST_SESSIONS.pop(
                bale_user_id,
                None
            )


            return await self.bale.send_message(
                bale_user_id,
                "Request submitted ✔️"
            )



        # =========================
        # MOVE NEXT
        # =========================

        session["step"] = next_step


        return await self._ask_next(
            bale_user_id
        )



    # =========================
    # NEXT QUESTION
    # =========================
    async def _ask_next(
        self,
        bale_user_id: str
    ):

        session = REQUEST_SESSIONS[bale_user_id]


        question = self.engine.get_question(
            session["type"],
            session["step"]
        )

        if (
        session["type"] == RequestType.LEAVE
        and session["step"] == "leave_type"
    ):
            return await self.bale.send_message(
            bale_user_id,
            question,
            keyboard=leave_types_keyboard()
        )


        if session["step"] in [
        "start_date",
        "end_date",
        "date"
    ]:

            now = datetime.now()

            return await self.bale.send_message(
            bale_user_id,
            question,
            keyboard=leave_calendar_keyboard(
                now.year,
                now.month
            )
        )

        return await self.bale.send_message(
            bale_user_id,
            question
        )
 
    # =========================
    # LIST METHODS
    # =========================
    async def show_my_requests(self, user_id: str):

        requests = await self.request_service.get_user_requests(user_id)
        
        return await self._format_list(user_id, requests)

    async def show_team_requests(self, manager_id: str):

        requests = await self.request_service.get_department_requests(manager_id)
        return await self._format_list(manager_id, requests)

    async def show_all_leave_requests(self, user_id: str):

        requests = await self.request_service.get_all_leave_requests()
        return await self._format_list2(user_id, requests)
    
    async def remained_leave_hours(self,user_id):
          return await self.request_service.remained_leave_hours(user_id)
    
    async def get_request_by_id(self,request_id):
          return await self.request_service.get_request_by_id(request_id)
    
    async def approve_request(self, request_id: str):

          updated_request = await self.request_service.approve_request(request_id)

          #await self.bale.send_message(
          #updated_request.manager_id,
          #"Request approved ✔️"
          #)

          return updated_request
    
    async def reject_request(self, request_id: str,reason: str):

          updated_request = await self.request_service.reject_request(request_id,reason)

          #await self.bale.send_message(
          #updated_request.manager_id,
          #"Request rejected ❌"
          #)

          return updated_request

    # =========================
    # FORMAT OUTPUT
    # =========================
    async def _format_list(self, user_id: str, requests):

        if not requests:
            return await self.bale.send_message(
                user_id,
                "No requests found"
            )

        for r in requests:

            body_text = "\n".join(
            [
                f"{key}: {value}"
                for key, value in r.data.items()
                if key != "medical_document"
            ]
        )

            user = await self.user_repository.get_by_id(r.user_id)
            manager = await self.user_repository.get_by_id(r.manager_id)

            message = (
            f"👤 کارمند: {user.first_name} {user.last_name}\n"
            f"📄 نوع درخواست: {r.type.value}\n"
            f"📝 جزئیات:\n{body_text}\n\n"
            f"📊 وضعیت: {r.status.value}\n"
            f"🕒 زمان ثبت درخواست: {r.created_at}"
            )

            keyboard = None

            if r.status == RequestStatus.PENDING:
               keyboard = request_action_keyboard(r.id)

        # ابتدا پیام درخواست + دکمه‌ها
            result = await self.bale.send_message(
            manager.bale_user_id,
            message,
            keyboard=keyboard
            )

            if keyboard:
               message_id = result["result"]["message_id"]
               r.message_id = str(message_id)
               await self.request_service.update(r)

        # سپس مدرک پزشکی
            medical = r.data.get("medical_document")

            if medical:
               await self.bale.send_document_by_file_id(
                chat_id=manager.bale_user_id,
                file_id=medical["file_id"],
                caption="📎 مدرک پزشکی"
                )


    async def _format_list2(self, user_id: str, requests):

        if not requests:
            return await self.bale.send_message(
                user_id,
                "No requests found"
            )

        for r in requests:

            body_text = "\n".join(
            [
                f"{key}: {value}"
                for key, value in r.data.items()
                if key != "medical_document"
            ]
            )

            user = await self.user_repository.get_by_id(r.user_id)
            message = (
            f"👤 کارمند: {user.first_name} {user.last_name}\n"
            f"📄 نوع درخواست: {r.type.value}\n"
            f"📝 جزئیات:\n{body_text}\n\n"
            f"📊 وضعیت: {r.status.value}\n"
            f"🕒 زمان ثبت درخواست: {r.created_at}"
            )

        # ابتدا اطلاعات درخواست
            await self.bale.send_message(
            user.bale_user_id,
            message
            )

        # سپس مدرک پزشکی
            medical = r.data.get("medical_document")

            if medical:
               await self.bale.send_document(
                chat_id=user.bale_user_id,
                file_id=medical["file_id"],
                caption="📎 مدرک پزشکی"
                )

            