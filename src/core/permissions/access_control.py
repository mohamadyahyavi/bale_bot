from src.modules.users.repository import UserRepository
from src.modules.departments.repository import DepartmentRepository

class AccessControlService:

    def __init__(self, user_repo: UserRepository, department_repo: DepartmentRepository):
        self.user_repo = user_repo
        self.department_repo = department_repo


    async def get_context(self, user_id):

        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise Exception("User not found")


        department = None
        is_manager = False

        if user.department_id:
            department = await self.department_repo.get_by_id(user.department_id)

            if department and department.manager_user_id == user.id:
                is_manager = True


        return {
            "user_id": user.id,
            "role": user.access_level,
            "department": department.name,
            "is_manager": is_manager
        }