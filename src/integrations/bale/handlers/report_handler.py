from datetime import date, timedelta

from src.modules.users.service import UserRepository
from src.modules.departments.repository import DepartmentRepository
from src.integrations.bale.client import BaleClient
from src.modules.requests.repository import RequestRepository
from src.integrations.kimai.service import KimaiService


class ReportHandler:

    def __init__(
        self,
        user_repository: UserRepository,
        department_repository:DepartmentRepository,
        kimai_service:KimaiService,
        request_repository:RequestRepository,
        bale_client: BaleClient
    ):
        self.user_repository = user_repository
        self.department_repository=department_repository
        self.kimai_service = kimai_service
        self.request_repository = request_repository
        self.bale = bale_client

    # =========================
    # MY REPORTS
    # =========================
    async def show_hr_reports(self, user_id: str):

        user = await self.user_repository.get_by_id(user_id)
        active_users = await self.user_repository.get_active_users()
        requests = await self.request_repository.get_month_approved_leaves()
        today = date.today()
        message = "📊 گزارش منابع انسانی\n\n"

        if requests:
           for req in requests:
               actor= await self.user_repository.get_by_id(req.user_id)
               body = req.data

               start = body.get("start_datetime")
               end = body.get("end_datetime")
               message += (
               f"\n درخواست مرخصی"           
               f"\n👤 {actor.first_name} {actor.last_name}"
               f"\n📅 شروع: {start}"
               f"\n📅 پایان: {end}\n"
               )


           await self.bale.send_message(user.bale_user_id, message)
           message="" 
           not_started_users = []   
           for active_user in active_users:
               
               has_started = await self.kimai_service.has_work_started_today(active_user.kimai_user_id)
               monthly_worked_hours = await self.kimai_service.get_month_worked_duration(active_user.kimai_user_id)
               monthly_delay_hours = await self.kimai_service.get_month_delay_hours(active_user.kimai_user_id)
               if not has_started:
                  not_started_users.append(active_user)

               message += (
               f"\n کارکرد ماه جاری"           
               f"\n👤 کارمند: {active_user.first_name} {active_user.last_name}"
               f"\n  ساعت: {monthly_worked_hours}"
               f"\n⏰ مجموع تأخیر ماه: {monthly_delay_hours} ساعت\n" 
               )
           await self.bale.send_message(user.bale_user_id,message)
           message=""
           if not_started_users:
              message += "❌ کارکنانی که امروز هنوز ساعت کاری ثبت نکرده‌اند:\n\n"
              for user in not_started_users:

                  message += (
                  f"👤 {user.first_name} {user.last_name}\n"
                  )
              await self.bale.send_message(
              hr.bale_user_id,
              message
              )

              

    # =========================
    # TEAM REPORTS (DAILY)
    # =========================
    async def show_team_daily_report(self, user_id: str):

        manager = await self.user_repository.get_by_id(user_id)

        department = await self.department_repository.get_by_manager_id(user_id)
        department_active_users = await self.user_repository.get_by_department_id(department.id)

        today = date.today()

        message = "👥 گزارش تیم (روزانه)\n\n"

        for member in department_active_users:

            worked = await self.kimai_service.has_work_started_today(member.kimai_user_id)
            message += f"👤 {member.first_name} {member.last_name}\n"
            if not worked:
               message += "📌 وضعیت: ❌ هنوز ساعت ثبت نکرده\n\n"
               continue
            worked_hours = await self.kimai_service.get_today_worked_duration(
            member.kimai_user_id
            )

            overtime = await self.request_repository.get_today_overtime_by_user_id(
            member.id
            )
            activities = await self.kimai_service.get_today_activity_durations(
            member.kimai_user_id
            )
            message += (
            f"⏱ کارکرد امروز: {worked_hours}\n"
            f"➕ اضافه‌کاری امروز: {overtime}\n\n"
            f"📋 فعالیت‌ها:\n"
            )
            if activities:
              for activity in activities:
                message += (
                    f"{activity['activity']} : {activity['duration']}\n"
                )
            else:
              message += " • فعالیتی ثبت نشده است.\n"

            message += "\n"

        await self.bale.send_message(
            manager.bale_user_id,
            message
        )

    async def show_team_weekly_report(self, user_id: str):

       manager = await self.user_repository.get_by_id(user_id)

       department = await self.department_repository.get_by_manager_id(user_id)
       department_active_users = await self.user_repository.get_by_department_id(
        department.id
       )

       message = "👥 گزارش هفتگی تیم\n\n"

       for member in department_active_users:

            worked_hours = await self.kimai_service.get_week_worked_duration(
            member.kimai_user_id
            )

            overtime = await self.request_repository.get_week_overtime_by_user_id(
            member.id
           )

            activities = await self.kimai_service.get_week_activity_durations(
            member.kimai_user_id
            )

            message += (
            f"👤 {member.first_name} {member.last_name}\n"
            f"⏱ کارکرد هفته: {worked_hours}\n"
            f"➕ اضافه‌کاری هفته: {overtime}\n"
            f"📋 فعالیت‌ها:\n"
        )

            if activities:
               for activity in activities:
                 message += (
                    f" {activity['activity']} : {activity['duration']}\n"
                 )
            else:
               message += "• فعالیتی ثبت نشده است.\n"

            message += "\n"

       await self.bale.send_message(
        manager.bale_user_id,
        message
        )

    async def show_team_monthly_report(self, user_id: str):

       manager = await self.user_repository.get_by_id(user_id)

       department = await self.department_repository.get_by_manager_id(user_id)
       department_active_users = await self.user_repository.get_by_department_id(
        department.id
       )

       message = "👥 گزارش ماهانه تیم\n\n"

       for member in department_active_users:

          worked_hours = await self.kimai_service.get_month_worked_duration(
            member.kimai_user_id
          )

          overtime = await self.request_repository.get_month_overtime_by_user_id(
            member.id
          )

          activities = await self.kimai_service.get_month_activity_duration(
            member.kimai_user_id
          )

          message += (
            f"👤 {member.first_name} {member.last_name}\n"
            f"⏱ کارکرد ماه: {worked_hours}\n"
            f"➕ اضافه‌کاری ماه: {overtime}\n"
            f"📋 فعالیت‌ها:\n"
          )

          if activities:
            for activity in activities:
                message += (
                    f" {activity['activity']} : {activity['duration']}\n"
                )
          else:
            message += "• فعالیتی ثبت نشده است.\n"

          message += "\n"

       await self.bale.send_message(
        manager.bale_user_id,
        message
       )

    async def show_my_monthly_report(self, user_id: str):

       user = await self.user_repository.get_by_id(user_id)


       message = "👥 گزارش ماهانه من\n\n"

       worked_hours = await self.kimai_service.get_month_worked_duration(
            user.kimai_user_id
          )

       activities = await self.kimai_service.get_month_activity_duration(
            user.kimai_user_id
          )

       message += (
            f"👤 {user.first_name} {user.last_name}\n"
            f"⏱ کارکرد ماه: {worked_hours}\n"
            f"📋 فعالیت‌ها:\n"
            )

       if activities:
            for activity in activities:
                message += (
                    f" {activity['activity']} : {activity['duration']}\n"
                )
       else:
            message += "• فعالیتی ثبت نشده است\n"

            message += "\n"

       await self.bale.send_message(
        user.bale_user_id,
        message
       )

    async def show_activity_report(self, user_id: str):

       user = await self.user_repository.get_by_id(user_id)

       activities = await self.kimai_service.get_activity_report()
       print(activities)

       message = "📊 گزارش Activity ماه جاری\n\n"


       if not activities:

        message += "• هیچ فعالیتی ثبت نشده است."

       else:

         for activity in activities:

            message += (
                f"📌 {activity['activity_name']}\n"
                f"⏱ زمان صرف شده: {activity['time']}\n\n"
            )


       await self.bale.send_message(
        user.bale_user_id,
        message
        )

    async def show_my_weekly_report(self, user_id: str):

       user = await self.user_repository.get_by_id(user_id)


       message = "👥 گزارش هفته جاری من\n\n"

       worked_hours = await self.kimai_service.get_week_worked_duration(
            user.kimai_user_id
          )

       activities = await self.kimai_service.get_week_activity_duration(
            user.kimai_user_id
          )

       message += (
            f"👤 {user.first_name} {user.last_name}\n"
            f"⏱ کارکرد هفته: {worked_hours}\n"
            f"📋 فعالیت‌ها:\n"
            )

       if activities:
            for activity in activities:
                message += (
                    f" {activity['activity']} : {activity['duration']}\n"
                )
       else:
            message += "• فعالیتی ثبت نشده است.\n"

            message += "\n"

       await self.bale.send_message(
        user.bale_user_id,
        message
       )

    async def show_my_daily_report(self, user_id: str):

        user = await self.user_repository.get_by_id(user_id)

        message = "👥 گزارش روزانه \n\n"

        message += f"👤 {user.first_name} {user.last_name}\n"
        
        worked_hours = await self.kimai_service.get_today_worked_duration(
            user.kimai_user_id
            )
        activities = await self.kimai_service.get_today_activity_durations(
            user.kimai_user_id
            )
        message += (
            f"⏱ کارکرد امروز: {worked_hours}\n"
            f"📋 فعالیت‌ها:\n"
            )
        if activities:
              for activity in activities:
                message += (
                    f"{activity['activity']} : {activity['duration']}\n"
                )
        else:
              message += " • فعالیتی ثبت نشده است.\n"

        message += "\n"

        await self.bale.send_message(
            user.bale_user_id,
            message
        )            

    
    # =========================
    # ALL REPORTS (ADMIN)
    # =========================
    async def show_all_reports(self, user_id: str):

        users = await self.user_service.get_active_users()

        today = date.today()

        message = "🏢 گزارش کل سازمان\n\n"

        for user in users:

            report = await self.report_service.daily(user, today)

            message += (
                f"👤 {user.first_name} {user.last_name}\n"
                f"⏱ {report.worked_hours}h | "
                f"⚠️ {report.missing_hours}h | "
                f"➕ {report.overtime_hours}h\n\n"
            )

        await self.bale.send_message(
            chat_id=user_id,
            text=message
        )

    # =========================
    # MONTHLY REPORT (USER)
    # =========================

    async def my_today_status_report(self,user_id):
          
        user = await self.user_repository.get_by_id(user_id)

        message = "👥 وضعیت امروز من\n\n"

        message += f"👤 {user.first_name} {user.last_name}\n"
        worked = await self.kimai_service.has_work_started_today(user.kimai_user_id)
        active_timer = await self.kimai_service.has_active_timer(user.kimai_user_id)
        if not worked:
           message += " .وضعیت: ❌ هنوز ساعت ثبت نکرده اید\n\n"   
        else:   
           worked_hours = await self.kimai_service.get_today_worked_duration(
             user.kimai_user_id
             )
           message += (
            f"⏱ کارکرد امروز: {worked_hours}\n")
        if not active_timer:
           message += " .وضعیت: ❌ شما تایمر فعال ندارید\n\n"
        else:
           message += " .وضعیت: شما تایمر فعال دارید\n\n"    

        await self.bale.send_message(
            user.bale_user_id,
            message
        )  