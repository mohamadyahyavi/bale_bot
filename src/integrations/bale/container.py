from sqlalchemy.ext.asyncio import AsyncSession

from src.integrations.bale.client import BaleClient
from src.integrations.bale.handlers.message_router import MessageRouter
from src.integrations.bale.handlers.user_handler import UserHandler
from src.integrations.bale.handlers.request_handler import RequestHandler
from src.integrations.bale.handlers.report_handler import ReportHandler

from src.modules.users.repository import UserRepository
from src.modules.requests.repository import RequestRepository
from src.modules.departments.repository import DepartmentRepository

from src.modules.users.service import UserService
from src.modules.requests.service import RequestService
from src.modules.notifications.service import NotificationService
from src.core.permissions.access_control import AccessControlService
from src.core.permissions.permission_service import PermissionService
from src.core.config import settings
from src.modules.reports.service import ReportService
from src.modules.reports.builder import ReportBuilder
from src.modules.reports.calculator import ReportCalculator


# =========================
# BUILD APPLICATION GRAPH
# =========================
def build_router(http_client, db: AsyncSession) -> MessageRouter:

    # -------------------------
    # CLIENTS
    # -------------------------
    bale_client = BaleClient(http_client)#settings.BALE_BOT_TOKEN)
    

    # -------------------------
    # REPOSITORIES
    # -------------------------
    user_repository = UserRepository(db)
    request_repository = RequestRepository(db)
    department_repository = DepartmentRepository(db)

    # -------------------------
    # SERVICES
    # -------------------------
    notification_service = NotificationService(bale_client)
    user_service = UserService(user_repository)
    request_service = RequestService(request_repository, user_repository, department_repository,notification_service)
    report_service=ReportService(ReportCalculator(),ReportBuilder())
    
    access_control_service = AccessControlService(
        user_repository,
        department_repository
    )

    permission_service = PermissionService(access_control_service)

    # -------------------------
    # HANDLERS
    # -------------------------
    user_handler = UserHandler(
        user_service=user_service,
        access_control_service=access_control_service,
        bale_client=bale_client
    )

    request_handler = RequestHandler(
        request_service=request_service,
        user_repository=user_repository,
        bale_client=bale_client
    )

    report_handler = ReportHandler(user_service,report_service,bale_client)

    # -------------------------
    # ROUTER (ENTRYPOINT)
    # -------------------------
    return MessageRouter(
        user_handler=user_handler,
        request_handler=request_handler,
        access_control_service=access_control_service,
        user_service=user_service,
        report_handler=report_handler,
        bale_client=bale_client
    )