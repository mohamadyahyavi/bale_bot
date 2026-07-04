from .user_handler import UserHandler
from .request_handler import RequestHandler
from src.modules.users.service import UserService
from src.modules.requests.enums import RequestType
from src.integrations.bale.client import BaleClient 
from .report_handler import ReportHandler
from src.integrations.bale.client import BaleClient 
from src.core.permissions.permission_service import PermissionService
from src.core.permissions.access_control import AccessControlService
REJECT_SESSIONS = {}

class MessageRouter:

    def __init__(self, user_handler:UserHandler, request_handler:RequestHandler,access_control_service: AccessControlService,user_service: UserService,report_handler:ReportHandler,bale_client:BaleClient):
        self.user_handler = user_handler
        self.request_handler = request_handler
        self.access_control_service = access_control_service
        self.user_service = user_service
        self.report_handler = report_handler
        self.bale_client=bale_client
        

    async def handle_callback(self, callback: dict):

          print("CALLBACK:", callback)

          data = callback.get("data")

          bale_user_id = str(
           callback.get("from", {}).get("id")
          )


          user = await self.user_service.get_by_bale_id(
          bale_user_id
          )


          if not user:
             return
          
          if not data:
              return 

          if data.startswith("approve_request:"):

             request_id = data.split(":")[1]

             print("APPROVE:", request_id)

             request = await self.request_handler.get_request_by_id(
             request_id
             )

             await self.request_handler.approve_request(
                request_id
             )


             if request.message_id:

                await self.bale_client.delete_message(
                bale_user_id,
                int(request.message_id)
                )


             return



          if data.startswith("reject_request:"):

             request_id = data.split(":")[1]

             print("REJECT:", request_id)

             request = await self.request_handler.get_request_by_id(request_id)
             if request.type == RequestType.LEAVE:

                REJECT_SESSIONS[bale_user_id] = request_id

                await self.bale_client.send_message(
                bale_user_id,
                "لطفا دلیل رد درخواست را ارسال کنید:"
                )
                return 

             await self.request_handler.reject_request(request_id,None)


             if request.message_id:

                await self.bale.delete_message(
                bale_user_id,
                int(request.message_id)
                )


             return


    async def handle(self, update: dict):

        print("MESSAGE ROUTER CALLED")

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

        if bale_user_id in REJECT_SESSIONS:

           request_id = REJECT_SESSIONS[bale_user_id]
           request = await self.request_handler.get_request_by_id(request_id)
           user= await self.user_service.get_by_id(request.user_id)
           #request.reject_reason=text
           #request=self.request_handler.update(request)


           await self.request_handler.reject_request(
           request_id,
           text
           )


           del REJECT_SESSIONS[bale_user_id]


           await self.bale_client.send_message(
           user.bale_user_id,
           f"دلیل:{text}"
           )


           return


        #print("bale_id:",bale_user_id)
        user = await self.user_service.get_by_bale_id(bale_user_id)
        #print("maaaaaaaaaaaaaaaaaaaaaaaard")
        
        if not user:
           return await self.user_handler.handle_start(bale_user_id)


        user_id = str(user.id)
        user_name=(user.first_name)
        #print("user_name:",user_name)

        accesses = await self.access_control_service.get_context(user_id)
        print("USER PERMISSIONS:")
        for key, value in accesses.items():
            print(f"{key}: {value}")
        print("mashti")

        if text == "/start":
            print("Hello-bale")
            return await self.user_handler.handle_start(bale_user_id)

        if text == "ثبت درخواست جدید":
           return await self.request_handler.start_flow(bale_user_id)
        
        if text == "درخواست های من":

           return await self.request_handler.show_my_requests(str(user_id))
        
        if text == "درخواست های تیم":

            if not accesses["is_manager"]:

               raise PermissionError(
              "You are not allowed to view team requests"
              )
            
            return await self.request_handler.show_team_requests(
                user_id
            )
        
        if text == "مانده مرخصی من":

           return await self.request_handler.remained_leave_hours(str(user_id))


        if text == "همه درخواست ها":


            if not accesses["role"]=="HR" or accesses["role"]=="CEO":
                    return await self.user_handler.handle_start(user_id)
            return await self.request_handler.show_all_requests(user_id)
        
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
            return await self.request_handler.handle_message(bale_user_id, text)
        
        if await self.request_handler.is_in_flow(
            user_id
        ):
            return await self.request_handler.handle_message(
                bale_user_id,
                text
            )

        return await self.request_handler.handle_message(bale_user_id, text)