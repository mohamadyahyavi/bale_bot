from src.integrations.bale.keyboards import request_types_keyboard
from src.modules.requests.enums import RequestType
from ..client import BaleClient
from .request_form_engine import RequestFormEngine
from src.modules.requests.service import RequestService

class RequestHandler:

    def __init__(self, request_service:RequestService, bale_client: BaleClient):

        self.request_service = request_service
        self.bale = bale_client

        self.engine = RequestFormEngine()

        # session storage (later move to Redis)
        self.sessions = {}

    # =========================
    # CHECK FLOW
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
            return await self.start_flow(user_id)

        # -------------------------
        # STEP 1: SELECT TYPE
        # -------------------------
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

        # -------------------------
        # STEP 2+: FORM FLOW
        # -------------------------

        step = session["step"]

        if not self.engine.validate(step, text):

            return await self.bale.send_message(
                user_id,
                f"Invalid value for {step}"
            )

        session["data"][step] = text

        # get next step
        next_step = self.engine.get_next_step(
            session["type"],
            step
        )

        # finished
        if next_step is None:

            await self.request_service.create_request(
                bale_user_id=user_id,
                request_data={
                    "type": session["type"],
                    "data": session["data"]
                }
            )

            self.sessions.pop(user_id, None)

            return await self.bale.send_message(
                user_id,
                "Request submitted ✔️"
            )

        # move next step
        session["step"] = next_step

        return await self._ask_next(user_id)

    # =========================
    # ASK QUESTION
    # =========================
    async def _ask_next(self, user_id: str):

        session = self.sessions[user_id]
        step = session["step"]

        questions = {
            "leave_type": "Daily or Hourly?",
            "start_datetime": "Enter start date/time:",
            "end_datetime": "Enter end date/time:",
            "reason": "Write reason:",
            "date": "Enter date:",
            "hours": "How many hours?",
            "destination": "Where is destination?"
        }

        return await self.bale.send_message(
            user_id,
            questions.get(step, f"Enter {step}:")
        )

    # =========================
    # VIEW METHODS
    # =========================
    async def show_my_requests(self, user_id: str):
        requests = await self.request_service.get_my_requests(user_id)

        return await self._format_list(user_id, requests)

    async def show_team_requests(self, user_id: str):
        requests = await self.request_service.get_team_requests(user_id)

        return await self._format_list(user_id, requests)

    async def show_all_requests(self, user_id: str):
        requests = await self.request_service.get_all_requests()

        return await self._format_list(user_id, requests)

    async def _format_list(self, user_id: str, requests):

        if not requests:
            return await self.bale.send_message(
                user_id,
                "No requests found"
            )

        text = "\n".join([
            f"{r.user.first_name} | {r.type} | {r.status}"
            for r in requests
        ])

        return await self.bale.send_message(user_id, text)