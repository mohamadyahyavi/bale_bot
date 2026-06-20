from datetime import datetime
from uuid import UUID
from .entity import RequestEntity
from .repository import RequestRepository
from ..users.repository import UserRepository
from ..users.service import UserService
from ..users.entity import User
from ..notifications.service import NotificationService

from .enums import (
    RequestStatus,RequestType
)



class RequestService:


    def __init__(
        self,
        request_repository:RequestRepository,
        user_repository:UserRepository,
        notification_service:NotificationService
    ):

        self.request_repository = request_repository

        self.user_repository = user_repository

        self.notification_service = notification_service



    async def create_request(
        self,
        bale_user_id: str,
        request_type,
        body: dict
    ):



        user = await self.user_repository.get_by_bale_id(

            bale_user_id

        )


        if not user:

            raise Exception(
                "User not found"
            )



        manager_id = (
            user.department.manager_user_id
        )



        request = RequestEntity(

            user_id=user.id,

            manager_id=manager_id,

            type=request_type,

            status=RequestStatus.PENDING.value,

            data=body

        )



        result = await self.request_repository.create(

            request

        )



        await self.notification_service.notify_new_request(

            manager_id,
            first_name=user.first_name,
            last_name=user.last_name,
            request_type=RequestType(request_type)

            "New request waiting for approval"

        )


        return result
    
    async def get_user_requests(
        self,
        user_id: UUID
    ):

        return await self.request_repository.get_by_user(
            user_id
        )



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


        return await self.request_repository.get_by_department(
            manager.department_id
        )
    
    async def approve_request(
        self,
        request_id: UUID
    ):

        request = await self.request_repository.get_by_id(
            request_id
        )


        if request.status != RequestStatus.PENDING.value:
            raise Exception("Invalid state")


        request.status = RequestStatus.ACCEPTED.value


        updated_request = await self.request_repository.update(
        request
    )
        
        user = await self.user_repository.get_by_id(
        request.user_id
    )

        if request.type == RequestType.LEAVE.value:

           data = request.data or {}

           start = data.get("start_datetime")
           end = data.get("end_datetime")

           if start and end:

              try:
                start_dt = datetime.fromisoformat(start)
                end_dt = datetime.fromisoformat(end)

                hours = (end_dt - start_dt).total_seconds() / 3600

              except Exception:
                raise Exception("Invalid datetime format")

              user.total_leave_hours = (
                (user.total_leave_hours or 0) + hours
            )

              await self.user_repository.update(user)

         
        await self.notification_service.notify_request_result(
        user_id=user.bale_user_id,

        first_name=user.first_name,

        last_name=user.last_name,

        request_type=RequestType(request.type),

        status=RequestStatus.ACCEPTED
    )
        
        hr = await self.user_repository.get_hr_users()

        await self.notification_service.notify_request_result(
                user_id=hr.bale_user_id,

            first_name=user.first_name,

            last_name=user.last_name,

            request_type=RequestType(request.type),

            status=RequestStatus.ACCEPTED
        )


        return updated_request





    async def reject_request(
        self,
        request_id: UUID
    ):

        request = await self.request_repository.get_by_id(
            request_id
        )


        if request.status != RequestStatus.PENDING.value:
            raise Exception("Invalid state")


        request.status = RequestStatus.REJECTED.value


    
        updated_request = await self.request_repository.update(
        request
    )
        
        user = await self.user_repository.get_by_id(
        request.user_id
    )
        
        await self.notification_service.notify_request_result(
        user_id=user.bale_user_id,

        first_name=user.first_name,

        last_name=user.last_name,

        request_type=RequestType(request.type),

        status=RequestStatus.ACCEPTED
    )
        
        hr = await self.user_repository.get_hr_users()

        await self.notification_service.notify_request_result(
                user_id=hr.bale_user_id,

            first_name=user.first_name,

            last_name=user.last_name,

            request_type=RequestType(request.type),

            status=RequestStatus.ACCEPTED
        )

        return updated_request