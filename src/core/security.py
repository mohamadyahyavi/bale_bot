from dataclasses import dataclass
from uuid import UUID

from src.modules.users.repository import UserRepository


# -------------------------
# CURRENT USER CONTEXT
# -------------------------
@dataclass
class CurrentUser:
    id: UUID
    bale_user_id: str
    access_level: str
    department_id: UUID | None = None


# -------------------------
# SECURITY SERVICE
# -------------------------
class SecurityService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


    async def get_user_by_bale_id(self, bale_user_id: str) -> CurrentUser:
        """
        Resolve Bale user → system user
        """

        user = await self.user_repository.get_by_bale_id(bale_user_id)

        if not user:
            return None


        return CurrentUser(
            id=user.id,
            bale_user_id=user.bale_user_id,
            access_level=user.access_level,
            department_id=user.department_id
        )


    async def is_user_active(self, bale_user_id: str) -> bool:
        """
        Optional helper for bot entry validation
        """

        user = await self.user_repository.get_by_bale_id(bale_user_id)

        if not user:
            return False

        return user.is_active