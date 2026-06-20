from src.integrations.bale.keyboards import request_types_keyboard,request_action_keyboard
from src.modules.requests.enums import RequestType
from src.integrations.bale.client import BaleClient
from .request_form_engine import RequestFormEngine
from src.modules.requests.service import RequestService


class RequestHandler:

    def __init__(
        self,
        request_service: RequestService,
        bale_client: BaleClient
    ):
        self.request_service = request_service
        self.bale = bale_client
        self.engine = RequestFormEngine()

        # session storage (later Redis)
        self.sessions: dict = {}

    # =========================
    # FLOW CHECK
    # =========================
    async def is_in_flow(self, user_id: str) -> bool:
        return user_id in self.sessions

    # =========================
    # START FLOW
    # =========================
    async def start_flow(self, user_id: str):

        self.sessions[user_id] = {
            "type": None,
            "step": None,
            "data": {}
        }

        return await self.bale.send_message(
            user_id,
            "Select request type:",
            keyboard=request_types_keyboard()
        )

    # =========================
    # MAIN HANDLER
    # =========================
    async def handle_message(self, user_id: str, text: str):

        session = self.sessions.get(user_id)

        if not session:
            return await self.bale.send_message(
                user_id,
                "Please start request flow first (/create_request)"
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
                    user_id,
                    "Invalid request type"
                )

            session["type"] = text
            session["step"] = self.engine.get_first_step(text)

            return await self._ask_next(user_id)

        # =========================
        # STEP 2+: FORM INPUT
        # =========================
        current_step = session["step"]

        if not self.engine.validate(current_step, text):
            return await self.bale.send_message(
                user_id,
                f"Invalid value for {current_step}"
            )

        # save answer
        session["data"][current_step] = text

        next_step = self.engine.get_next_step(
            session["type"],
            current_step
        )

        # =========================
        # FINISH FLOW
        # =========================
        if next_step is None:

            await self.request_service.create_request(
                bale_user_id=user_id,
                request_type=session["type"],
                body=session["data"]
            )

            self.sessions.pop(user_id, None)

            return await self.bale.send_message(
                user_id,
                "Request submitted ✔️"
            )

        # move next
        session["step"] = next_step
        return await self._ask_next(user_id)

    # =========================
    # NEXT QUESTION
    # =========================
    async def _ask_next(self, user_id: str):

        session = self.sessions[user_id]

        question = self.engine.get_question(
            session["type"],
            session["step"]
        )

        return await self.bale.send_message(
            user_id,
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

    async def show_all_requests(self, user_id: str):

        requests = await self.request_service.get_all_requests()
        return await self._format_list(user_id, requests)
    
    async def approve_request(self, request_id: str):

          updated_request = await self.request_service.approve_request(request_id)

          await self.bale.send_message(
          updated_request.manager_id,
          "Request approved ✔️"
          )

          return updated_request
    
    async def reject_request(self, request_id: str):

          updated_request = await self.request_service.reject_request(request_id)

          await self.bale.send_message(
          updated_request.manager_id,
          "Request rejected ❌"
          )

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
            ]
        )


            message = (
            "📌 درخواست جدید\n\n"
            f"👤 کارمند: {r.user.first_name} {r.user.last_name}\n"
            f"📄 نوع درخواست: {r.type}\n\n"
            f"📝 جزئیات:\n{body_text}\n\n"
            f"📊 وضعیت: {r.status}"
        )


            await self.bale.send_message(
            user_id,
            message,
            keyboard=request_action_keyboard(r.id)
        )