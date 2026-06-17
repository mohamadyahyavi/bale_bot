from src.integrations.bale.client import BaleClient

from src.integrations.bale.handlers.message_router import MessageRouter

from src.modules.users.service import UserService
from src.modules.users.repository import UserRepository
from src.integrations.bale.handlers.user_handler import UserHandler

from src.core.permissions.permission_service import PermissionService
from src.core.permissions.access_control import AccessControlService


from src.db.session import AsyncSessionLocal

import httpx



async def get_bale_client():

    http_client = httpx.AsyncClient(

        base_url=(
            f"{settings.BALE_API_URL}"
            f"{settings.BALE_BOT_TOKEN}"
        )
    )

    return BaleClient(
        http_client
    )



async def get_user_service():

    session = AsyncSessionLocal()

    user_repository = UserRepository(
        session
    )


    return UserService(
        user_repository
    )



async def get_permission_service():

    session = AsyncSessionLocal()


    access_control = AccessControlService(
        session
    )


    return PermissionService(
        access_control
    )



async def get_message_router():

    
    bale_client = await get_bale_client()


    user_service = await get_user_service()


    permission_service = await get_permission_service()



    user_handler = UserHandler(
        user_service,
        permission_service,
        bale_client
    )


    return MessageRouter(
        user_handler
    )