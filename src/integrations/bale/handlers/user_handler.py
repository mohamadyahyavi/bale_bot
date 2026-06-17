from src.core.permissions.permission_service import PermissionService
from src.modules.users.service import UserService
from src.integrations.bale.client import BaleClient as bale
class UserHandler:

    def __init__(self, user_service:UserService,permission_service:PermissionService, bale_client:bale):
        self.user_service = user_service
        self.permission_service = permission_service
        self.bale = bale_client

    async def handle_start(self, bale_user_id: str):

        user = await self.user_service.get_by_bale_id(bale_user_id)

        if not user:
            return await self.bale.send_message(
                bale_user_id,
                "User not registered"
            )
        
        permissions = await self.permission_service.get_permissions(
            bale_user_id
        )

        menu = self._build_menu(permissions)

        return await self.bale.send_message(
            bale_user_id,
            f"Welcome {user.first_name}",
            keyboard=menu
        )

    def _build_menu(self, permissions):

        menu = []


        if permissions["can_create_request"]:
            menu.append(["Request New"])


        if permissions["can_view_own_requests"]:
            menu.append(["My Requests"])


        if permissions["can_view_department_requests"]:
            menu.append(["Department Requests"])


        if permissions["can_view_all_requests"]:
            menu.append(["All Requests"])


        if permissions["can_view_own_reports"]:
            menu.append(["My Reports"])


        if permissions["can_view_team_reports"]:
            menu.append(["Team Reports"])


        if permissions["can_view_all_reports"]:
            menu.append(["Reports"])


        return {"keyboard": menu,
                "resize_keyboard": True
                }