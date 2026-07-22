from src.core.permissions.permission_service import PermissionService
from src.core.permissions.access_control import AccessControlService
from src.modules.users.service import UserService
from src.integrations.bale.client import BaleClient as bale
from src.integrations.bale.keyboards import employee_keyboard,hr_keyboard,ceo_keyboard,manager_keyboard,my_reports_keyboard
class UserHandler:

    def __init__(self, user_service:UserService,access_control_service:AccessControlService, bale_client:bale):
        self.user_service = user_service
        self.access_control_service = access_control_service
        self.bale = bale_client

    async def handle_start(self, bale_user_id: str):

        user = await self.user_service.get_by_bale_id(bale_user_id)

        if not user:
            return await self.bale.send_message(
                bale_user_id,
                "User not registered"
            )
        
        context = await self.access_control_service.get_context(
            user.id
        )

        menu = self._build_menu(context)

        return await self.bale.send_message(
            bale_user_id,
            f"Welcome {user.first_name}",
            keyboard=menu
        )

    def _build_menu(self, context):

        if context["role"] == "CEO":
            return ceo_keyboard()
        
        if context["is_manager"]:
            return manager_keyboard() 
        

        if context["role"] == "HR":
            return hr_keyboard()
     
              
        return employee_keyboard()