from .user_handler import UserHandler
from .request_handler import RequestHandler
from src.modules.users.service import UserService
from src.modules.requests.enums import RequestType
from src.integrations.bale.client import BaleClient 
from .report_handler import ReportHandler
from src.integrations.bale.client import BaleClient
from src.integrations.kimai.service import KimaiService 
from .time_entry_handler import TimeEntryHandler
from src.core.permissions.permission_service import PermissionService
from src.core.permissions.access_control import AccessControlService
from src.integrations.bale.keyboards import team_reports_keyboard,projects_keyboard,my_reports_keyboard
from src.integrations.bale.calendar_keyboard import (
    leave_calendar_keyboard,
    previous_month,
    next_month,
)
from .overtime_report_handler import OvertimeReportHandler
from .user_registry_handler import UserRegistrationHandler
from src.integrations.bale.handlers.request_handler import REQUEST_SESSIONS

REJECT_SESSIONS = {}
TIME_ENTRY_SESSIONS = {}
#REQUEST_SESSIONS = {}


class MessageRouter:

    def __init__(self, user_handler:UserHandler,user_registration_handler: UserRegistrationHandler,kimai_service:KimaiService,time_entry_handler:TimeEntryHandler, request_handler:RequestHandler,overtime_report_handler: OvertimeReportHandler,access_control_service: AccessControlService,user_service: UserService,report_handler:ReportHandler,bale_client:BaleClient):
        self.user_handler = user_handler
        self.user_registration_handler = user_registration_handler
        self.kimai_service = kimai_service
        self.time_entry_handler = time_entry_handler
        self.request_handler = request_handler
        self.overtime_report_handler = overtime_report_handler
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

          if data.startswith("cal_prev:"):

             _, year, month = data.split(":")
        
             year = int(year)
             month = int(month)

             year, month = previous_month(year, month)

             return await self.bale_client.send_message(
                          bale_user_id,
                          "📅 تاریخ را انتخاب کنید:",
                          keyboard=leave_calendar_keyboard(year, month))

          if data.startswith("cal_next:"):

             _, year, month = data.split(":")

             year = int(year)
             month = int(month)

             year, month = next_month(year, month)

             return await self.bale_client.send_message(
             bale_user_id,
             "📅 تاریخ را انتخاب کنید:",
             keyboard=leave_calendar_keyboard(year, month)
    )
          if data.startswith("cal_day:"):
              print("ENTERED CAL_DAY")

              session = REQUEST_SESSIONS.get(bale_user_id)

              print("SESSION =", session)

              if not session:
                 print("SESSION IS NONE")
                 return

              print("CURRENT STEP =", session["step"])

              _, year, month, day = data.split(":")

              selected_date = f"{year}-{int(month):02d}-{int(day):02d}"

              session = REQUEST_SESSIONS.get(bale_user_id)

              if not session:
                 return

              current_step = session["step"]

    # ذخیره تاریخ انتخاب شده
              session["data"][current_step] = selected_date

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
                next_step = self.request_handler.engine.get_next_step(
                session["type"],
                current_step
                )

              
              if next_step is None:

                await self.request_handler.request_service.create_request(
                bale_user_id=bale_user_id,
                request_type=session["type"],
                body=session["data"]
                )

                REQUEST_SESSIONS.pop(bale_user_id, None)

                return await self.bale_client.send_message(
                bale_user_id,
                "Request submitted ✔️"
                )

    # رفتن به مرحله بعد
              session["step"] = next_step

              return await self.request_handler._ask_next(
              bale_user_id
              )
           

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

        #projects= await self.kimai_service.get_all_projects()
        if text == "/start":
            print("Hello-bale")
            return await self.user_handler.handle_start(bale_user_id)

        if text == "ثبت درخواست جدید":
           return await self.request_handler.start_flow(bale_user_id)
        
        if text == "ثبت ساعت و پروژه":

            #await self.bale_client.send_message(
            #bale_user_id,
            #"پروژه مورد نظر خود را انتخاب کنید:",
            #keyboard=projects_keyboard(projects)
            #)
            return await self.time_entry_handler.start_flow(
            bale_user_id
            )

        
        if text == "گزارش روزانه تیم":

           if not accesses["is_manager"]:
              return await self.user_handler.handle_start(bale_user_id)

           return await self.report_handler.show_team_daily_report(
           user_id
           )
        
        if text == "کارکرد و تاخیر های من":

            return await self.report_handler.my_monthly_work_and_delay(user_id)
    

        if text == "گزارش هفتگی تیم":

           if not accesses["is_manager"]:
              return await self.user_handler.handle_start(bale_user_id)

           return await self.report_handler.show_team_weekly_report(
               user_id
           )
        
        if text == "درخواست های تیم":

            return await self.request_handler.show_team_requests(user_id)


        if text == "گزارش ماهانه تیم":

           if not accesses["is_manager"]:
              return await self.user_handler.handle_start(bale_user_id)

           return await self.report_handler.show_team_monthly_report(
            user_id
           )
        if text == "گزارش های اضافه کاری":

           if accesses["role"] != "HR":
              return await self.user_handler.handle_start(
              bale_user_id
              )

           return await self.overtime_report_handler.show_last_30_days_reports(
           bale_user_id
           )


        if text == "🔙 بازگشت":

           return await self.user_handler.handle_start(
           bale_user_id
        )
              
        
        if text == "گزارش های من":

            return await self.bale_client.send_message(
            bale_user_id,
            "نوع گزارش را انتخاب کنید:",
            keyboard=my_reports_keyboard()
            )

        if text == "مشاهده لاگ ها" :
           return await self.report_handler.show_logs(bale_user_id)

        if text == "افزودن کاربر جدید":

           if accesses["role"] != "ADMIN":
              return await self.user_handler.handle_start(
              bale_user_id
           )

           return await self.user_registration_handler.start_flow(
           bale_user_id
           )

               
        if text =="گزارش منابع انسانی":

            return await self.report_handler.show_hr_reports(user_id)
        
        if text == "گزارش های تیم":

            return await self.bale_client.send_message(
            bale_user_id,
            "نوع گزارش را انتخاب کنید:",
            keyboard=team_reports_keyboard()
            )


        if text == "گزارش ماهانه":
        
            return await self.report_handler.show_my_monthly_report(
                user_id
            )
        
        if text == "گزارش هفتگی":
        
            return await self.report_handler.show_my_weekly_report(
                user_id
            )
        
        if text == "گزارش فعالیت ها":

           #if not accesses["is_manager"] or accesses["role"]=="HR" :
             # return await self.user_handler.handle_start(bale_user_id)
           return await self.report_handler.show_activity_report(user_id)
                

        
        if text == "گزارش روزانه":
        
            return await self.report_handler.show_my_daily_report(
                user_id
            )
        
        if text == "وضعیت امروز من":
        
            return await self.report_handler.my_today_status_report(
                user_id
            )
        
        if text == "گزارش های اضافه کاری تیم":

           if not accesses["is_manager"]:
              raise PermissionError(
              "You are not allowed to view team overtime reports"
           )

           return await self.overtime_report_handler.show_team_last_30_days_reports(
           bale_user_id
           )

        if text == "All Reports":
            if not permissions["can_view_all_reports"]:
                return await self.user_handler.handle_start(user_id)
            return await self.report_handler.show_all_reports(
                user_id
            )
        
        if text == "ارسال گزارش اضافه کاری":

           return await self.overtime_report_handler.start_flow(
           bale_user_id
           )
        

        if await self.time_entry_handler.is_in_flow(bale_user_id):
           return await self.time_entry_handler.handle_message(
           bale_user_id,
           text
        )

        if await self.overtime_report_handler.is_in_flow(
            bale_user_id
        ):
            return await self.overtime_report_handler.handle_message(
                bale_user_id,
                message
            )
        
        if await self.request_handler.is_in_flow(bale_user_id):
           return await self.request_handler.handle_message(
           bale_user_id,
           message
        )

        if await self.user_registration_handler.is_in_flow(bale_user_id):
           return await self.user_registration_handler.handle_message(bale_user_id,message)

        if text in ["LEAVE", "REMOTE", "OVERTIME", "MISSION"]:
            return await self.request_handler.handle_message(bale_user_id, message)

        return await self.user_handler.handle_start(bale_user_id)