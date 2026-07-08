from datetime import datetime
from uuid import UUID
from .entity import RequestEntity
from .repository import RequestRepository
from ..users.repository import UserRepository
from ..users.service import UserService
from ..users.entity import User
from ..notifications.service import NotificationService
from ..departments.repository import DepartmentRepository

from .enums import (
    RequestStatus,RequestType
)



class RequestService:


    def __init__(
        self,
        request_repository:RequestRepository,
        user_repository:UserRepository,
        department_repository:DepartmentRepository,
        notification_service:NotificationService
        ):

        self.request_repository = request_repository
        self.user_repository = user_repository
        self.department_repository= department_repository
        self.notification_service = notification_service



    async def create_request(
       self,
       bale_user_id: str,
       request_type,
       body: dict
       ):

       user = await self.user_repository.get_by_bale_id(bale_user_id)

       if not user:
          raise Exception("User not found")

    # =========================
    # SAFE DEPARTMENT LOADING
    # =========================
       department = None
       manager_id = None

       if user.department_id:
           department = await self.department_repository.get_by_id(user.department_id)

       if department:
           manager_id = department.manager_user_id

       if not manager_id:
           raise Exception("Manager not found for this user")
       
       manager=await self.user_repository.get_by_id(manager_id)


    # =========================
    # CREATE REQUEST
    # =========================
       if isinstance(request_type, str):
          request_type = RequestType(request_type)
       request = RequestEntity(
        user_id=user.id,
        manager_id=manager_id,
        type=request_type,
        status=RequestStatus.PENDING.value,
        data=body
      )

       result = await self.request_repository.create(request)

    # =========================
    # NOTIFICATION
    # =========================
       await self.notification_service.notify_new_request(
        manager.bale_user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        request_type=RequestType(request_type)
        )
       await self.notification_service.notify_new_request(
        user.bale_user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        request_type=RequestType(request_type)
        )

       return result
    
    async def get_user_requests(
        self,
        user_id: UUID
    ):

        return await self.request_repository.get_by_user(
            user_id
        )
    
    async def get_request_by_id(self,request_id):
          return await self.request_repository.get_by_id(request_id)


    async def get_department_requests(
        self,
        manager_id: UUID
        ):

        manager = await self.user_repository.get_by_id(
            manager_id
        )

        if not manager:
            raise Exception(
                "Manager not found"
            )


        return await self.request_repository.get_by_manager(
            manager.id
        )
    
    async def approve_request(
        self,
        request_id: UUID
    ):

        request = await self.request_repository.get_by_id(
            request_id
        )

        print("REQUEST STATUS:", request.status)
        print("TYPE:", type(request.status))
        if request.status != RequestStatus.PENDING:
            raise Exception("Invalid state")


        request.status = RequestStatus.ACCEPTED
        request.processed_at = datetime.now()


        updated_request = await self.request_repository.update(
        request
    )
        
        user = await self.user_repository.get_by_id(
        request.user_id
    )

        if request.type == RequestType.LEAVE:

           data = request.data or {}

           start = data.get("start_datetime")
           end = data.get("end_datetime")
           leave_type = data.get("leave_type")

           if start and end:

              try:
                start_dt = datetime.fromisoformat(start)
                end_dt = datetime.fromisoformat(end)

              except Exception:
                raise Exception("Invalid datetime format")
              
              if end_dt <= start_dt:
                 raise Exception("End datetime must be after start datetime")


              hours=0 

              if leave_type == "DAILY":

                duration_hours = (end_dt - start_dt).total_seconds() / 3600

                leave_days = duration_hours / 24

                hours = leave_days * 7

              elif leave_type == "HOURLY":

                   if start_dt.date() == end_dt.date():

                      hours = (
                      end_dt - start_dt
                      ).total_seconds() / 3600
                   else:
                # اگر ساعتی از چند روز رد شد
                # هر روز 7 ساعت
                       days = (
                       end_dt.date() - start_dt.date()
                       ).days

                       hours = days * 7

              print("REQUESTED LEAVE HOURS:",hours)         


              current_leave = user.total_leave_hours or 0

              if current_leave + hours > 182:

                 return await self.notification_service.notify_leave_limit_reached(user.bale_user_id)
                 raise Exception("Leave limit exceeded")     

              user.total_leave_hours = (
                 current_leave + hours
                )

              await self.user_repository.update(user)

         
        await self.notification_service.notify_request_result(
        user_bale_id=user.bale_user_id,

        first_name=user.first_name,

        last_name=user.last_name,

        request_type=RequestType(request.type),

        status=RequestStatus.ACCEPTED
    )
        
        hr = await self.user_repository.get_hr_user() 

        await self.notification_service.notify_request_result(
                user_bale_id=hr.bale_user_id,

            first_name=user.first_name,

            last_name=user.last_name,

            request_type=RequestType(request.type),

            status=RequestStatus.ACCEPTED
        )


        return updated_request



    async def reject_request(
        self,
        request_id: UUID,
        reason:str
    ):

        request = await self.request_repository.get_by_id(
            request_id
        )


        if request.status != RequestStatus.PENDING:
            raise Exception("Invalid state")

        request.status = RequestStatus.REJECTED
        request.processed_at = datetime.now()
        request.reject_reason = reason

        print(reason)
   
        updated_request = await self.request_repository.update(
        request
        )
        
        user = await self.user_repository.get_by_id(
        request.user_id
        )
        
        await self.notification_service.notify_request_result(
        user_bale_id=user.bale_user_id,

        first_name=user.first_name,

        last_name=user.last_name,

        request_type=RequestType(request.type),

        status=RequestStatus.REJECTED
    )
        
        hr = await self.user_repository.get_hr_user()

        await self.notification_service.notify_request_result(
                user_bale_id=hr.bale_user_id,

            first_name=user.first_name,

            last_name=user.last_name,

            request_type=RequestType(request.type),

            status=RequestStatus.REJECTED
        )

        return updated_request
    
    async def update(self,request):
          await self.request_repository.update(request)


    async def remained_leave_hours(self,user_id):

          user= await self.user_repository.get_by_id(user_id) 
          hours=182-user.total_leave_hours
          return await self.notification_service.notify_leave_hours(user.bale_user_id,hours)
    

    async def get_all_leave_requests(self):

          return await self.request_repository.get_all_leave_requests()


    async def get_month_approved_leaves_total(self) -> float:

        leaves = await self.request_repository.get_month_approved_leaves()

        total_hours = 0

        for leave in leaves:
            data = leave.data or {}

            start = data.get("start_datetime")
            end = data.get("end_datetime")
            leave_type = data.get("leave_type")

            if not start or not end:
               continue

            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)

            if leave_type == "DAILY":
               duration_hours = (end_dt - start_dt).total_seconds() / 3600
               total_hours += (duration_hours / 24) * 7

            elif leave_type == "HOURLY":
                total_hours += (end_dt - start_dt).total_seconds() / 3600

            return round(total_hours, 2)  

