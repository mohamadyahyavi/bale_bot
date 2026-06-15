from datetime import datetime

from .entity import RequestEntity

from .enums import (
    RequestStatus
)



class RequestService:



    def __init__(
        self,
        request_repository,
        user_repository,
        notification_service
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


        if not manager_id:

            raise Exception(
                "Manager not found"
            )



        request = RequestEntity(

            user_id=user.id,

            manager_id=manager_id,

            type=request_type,

            status=RequestStatus.PENDING,

            data=body

        )



        result = await self.request_repository.create(

            request

        )



        await self.notification_service.notify_user(

            manager_id,

            "New request waiting for approval"

        )


        return result