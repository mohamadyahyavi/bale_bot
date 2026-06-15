from src.integrations.bale.keyboards import request_types_keyboard


class RequestHandler:

    def __init__(self, request_service, bale_client):
        self.request_service = request_service
        self.bale = bale_client
        self.sessions = {}

    # -------------------------
    # شروع ایجاد درخواست
    # -------------------------
    async def start_flow(self, user_id: str):

        self.sessions[user_id] = {
            "step": "choose_type",
            "data": {}
        }

        return await self.bale.send_message(
            user_id,
            "Select request type:",
            keyboard=request_types_keyboard()
        )

    # -------------------------
    # ادامه flow
    # -------------------------
    async def handle_message(self, user_id: str, text: str):

        session = self.sessions.get(user_id)

        if not session:
            return await self.start_flow(user_id)

        step = session["step"]

        # -------------------------
        # STEP 1: choose type
        # -------------------------
        if step == "choose_type":

            session["data"]["type"] = text
            session["step"] = "fill_body"

            return await self.bale.send_message(
                user_id,
                "Now write details of your request:"
            )

        # -------------------------
        # STEP 2: fill body
        # -------------------------
        if step == "fill_body":

            session["data"]["body"] = text

            await self.request_service.create_request(
                bale_user_id=user_id,
                data=session["data"]
            )

            self.sessions.pop(user_id)

            # ارسال تایید به کاربر
            await self.bale.send_message(
                user_id,
                "Request submitted ✔️"
            )

            return