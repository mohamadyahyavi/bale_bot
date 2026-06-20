from uuid import UUID
from .entity import User
from .repository import UserRepository

class UserService:


    def __init__(
        self,
        user_repository:UserRepository
    ):
        self.user_repository = user_repository



    async def get_by_bale_id(
        self,
        bale_user_id: str
    ):

        return await self.user_repository.get_by_bale_id(
            bale_user_id
        )



    async def get_user_menu_role(
        self,
        bale_user_id: str
    ):

        user = await self.user_repository.get_by_bale_id(
            bale_user_id
        )


        if not user:
            raise Exception(
                "User not found"
            )


        is_manager = False


        if user.department:

            is_manager = (
                user.department.manager_user_id
                == user.id
            )


        return {

            "access_level": user.access_level,

            "is_manager": is_manager

        }



    async def get_department_users(
        self,
        department_id: UUID
    ):

        return await self.user_repository.get_by_department_id(
            department_id
        )



    async def get_hr_user(self):

        return await self.user_repository.get_hr_users()



    async def can_manage_request(
        self,
        manager_id: UUID,
        request_manager_id: UUID
    ):


        return (
            manager_id == request_manager_id
        )