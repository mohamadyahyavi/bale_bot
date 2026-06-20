from .user_handler import UserHandler
from .request_handler import RequestHandler
from src.modules.users.service import UserService
##from .approval_handler import ApprovalHandler
from .report_handler import ReportHandler
from src.core.permissions.permission_service import PermissionService


class MessageRouter:

    def __init__(self, user_handler:UserHandler, request_handler:RequestHandler,permission_service: PermissionService,user_service: UserService):
        self.user_handler = user_handler
        self.request_handler = request_handler
        self.permission_service = permission_service
        self.user_service = user_service
        #self.report_handler = report_handler

    async def handle_callback(self, callback: dict):

          data = callback.get("data")
          bale_user_id = str(callback.get("from", {}).get("id"))

          user = await self.user_service.get_by_bale_id(bale_user_id)
          if not user:
             return

          user_id = str(user.id)

          if data.startswith("approve_request:"):
             request_id = data.split(":")[1]
             return await self.request_handler.approve_request(request_id)

          if data.startswith("reject_request:"):
             request_id = data.split(":")[1]
             return await self.request_handler.reject_request(request_id)    

    async def handle(self, update: dict):

        if "callback_query" in update:
            return await self.handle_callback(update["callback_query"])


    # =========================
    # MESSAGE HANDLER
    # =========================
        message = update.get("message")
        if not message:
             return

        text = message.get("text", "")
        bale_user_id = str(message.get("from", {}).get("id"))

        user = await self.user_service.get_by_bale_id(bale_user_id)
        if not user:
                 return await self.user_handler.handle_start(bale_user_id)

        user_id = str(user.id)

        permissions = await self.permission_service.get_permissions(user_id)

        if text == "/start":
            return await self.user_handler.handle_start(str(user_id))

        if text == "/create_request":
            return await self.request_handler.start_flow(str(user_id))
        
        if text == "My Requests":

           return await self.request_handler.show_my_requests(str(user_id))
        
        if text == "Team Requests":
            if not permissions["can_view_department_requests"]:
               return await self.user_handler.handle_start(user_id)
            return await self.request_handler.show_team_requests(
                user_id
            )

        if text == "All Requests":


            if not permissions["can_view_all_requests"]:
                    return await self.user_handler.handle_start(user_id)
            return await self.request_handler.show_all_requests(
                user_id
            )
        
        if text == "My Reports":

            if not permissions["can_view_my_reports"]:
                return await self.user_handler.handle_start(user_id)
            return await self.report_handler.show_my_reports(
                user_id
            )

        if text == "Team Reports":
            if not permissions["can_view_team_reports"]:
                return await self.user_handler.handle_start(user_id)
            return await self.report_handler.show_team_reports(
                user_id
            )

        if text == "All Reports":
            if not permissions["can_view_all_reports"]:
                return await self.user_handler.handle_start(user_id)
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