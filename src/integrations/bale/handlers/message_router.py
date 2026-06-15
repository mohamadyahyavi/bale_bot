class MessageRouter:

    def __init__(self,user_handler,request_handler, approval_handler):
        self.user_handler = None
        self.request_handler = None
        self.approval_handler = None

    async def handle(self, update: dict):

        message = update.get("message", {})
        text = message.get("text", "")
        user_id = message.get("from", {}).get("id")

        # ساده‌ترین routing
        if text.startswith("/start"):
            return await self.user_handler.handle_start(user_id)

        if text.startswith("/create_request"):
            return await self.request_handler.start_flow(user_id)
        
        if text in [
            "LEAVE",
            "REMOTE",
            "OVERTIME",
            "MISSION"
        ]:
            return await self.request_handler.handle_message(
                user_id,
                text
            )


        return await self.request_handler.handle_message(
            user_id,
            text
        )

        