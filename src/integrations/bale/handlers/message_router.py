from .user_handler import UserHandler
from .request_handler import RequestHandler
##from .approval_handler import ApprovalHandler
from .report_handler import ReportHandler


class MessageRouter:

    def __init__(self, user_handler:UserHandler, request_handler:RequestHandler, report_handler:ReportHandler):
        self.user_handler = user_handler
        self.request_handler = request_handler
        self.report_handler = report_handler

    async def handle(self, update: dict):

        message = update.get("message")

        if not message:
            return

        text = message.get("text", "")
        user_id = message.get("from", {}).get("id")

        if not user_id:
            return

        if text == "/start":
            return await self.user_handler.handle_start(str(user_id))

        if text == "/create_request":
            return await self.request_handler.start_flow(str(user_id))
        
        if text == "My Requests":

           return await self.request_handler.show_my_requests(str(user_id))
        
        if text == "Team Requests":
            return await self.request_handler.show_team_requests(
                user_id
            )

        if text == "All Requests":
            return await self.request_handler.show_all_requests(
                user_id
            )
        
        if text == "My Reports":
            return await self.report_handler.show_my_reports(
                user_id
            )

        if text == "Team Reports":
            return await self.report_handler.show_team_reports(
                user_id
            )

        if text == "All Reports":
            return await self.report_handler.show_all_reports(
                user_id
            )

        if text in ["LEAVE", "REMOTE", "OVERTIME", "MISSION"]:
            return await self.request_handler.handle_message(str(user_id), text)
        
        if await self.request_handler.is_in_flow(
            user_id
        ):
            return await self.request_handler.handle_message(
                user_id,
                text
            )

        return await self.request_handler.handle_message(str(user_id), text)