from sqlalchemy.ext.asyncio import async_sessionmaker

from src.integrations.bale.client import BaleClient

from src.integrations.kimai.client import KimaiClient
from src.integrations.kimai.service import KimaiService
from src.modules.requests.repository import RequestRepository
from src.modules.users.repository import UserRepository
from src.jobs.contract_expiry import ContractExpiryJob
from src.modules.notifications.service import NotificationService

from src.modules.reports.service import ReportService
from src.modules.reports.calculator import ReportCalculator
from src.modules.reports.builder import ReportBuilder

from src.jobs.work_start_reminder import WorkStartReminderJob
from src.jobs.missing_hours import MissingHoursJob
from src.jobs.open_timer_check import OpenTimerCheckJob
from src.jobs.pending_requests import PendingRequestsJob
from src.jobs.start_work import WorkStartNotificationJob
from src.jobs.finish_work import WorkEndNotificationJob
from .setup import setup_scheduler
from src.core.scheduler import SchedulerManager
from src.core.config import settings

def build_scheduler_jobs(
    http_client,
    session_factory: async_sessionmaker
):
    print("BUILD SCHEDULER CALLED")
    # =========================
    # CLIENTS
    # =========================
    bale_client = BaleClient(http_client)
    kimai_client = KimaiClient(
    base_url=settings.KIMAI_BASE_URL,
    token=settings.KIMAI_API_TOKEN,
)

    #kimai_client = KimaiClient()

    # =========================
    # REPOSITORIES
    # =========================

    #user_repository = UserRepository(db)
    #request_repository = RequestRepository(db)
    async def get_user_repository():

        async with session_factory() as db:

            return UserRepository(db)



    async def get_request_repository():

        async with session_factory() as db:

            return RequestRepository(db)
    # =========================
    # SERVICES
    # =========================

    notification_service = NotificationService(
        bale_client
    )


    kimai_service = KimaiService(
       kimai_client
    )


    report_service = ReportService(
       # kimai_service,
        ReportCalculator(),
        ReportBuilder()
    )

    # =========================
    # JOBS
    # =========================
    work_start_job = WorkStartReminderJob(
        session_factory,
        kimai_service,
        notification_service
    )


    missing_hours_job = MissingHoursJob(
        session_factory,
        report_service,
        notification_service
    )


    open_timer_job = OpenTimerCheckJob(
        session_factory,
        kimai_service,
        notification_service
    )


    contract_expiry_job = ContractExpiryJob(
    session_factory,
    notification_service
    )
    
    start_work_job=WorkStartNotificationJob(session_factory,notification_service)
    finish_work_job=WorkEndNotificationJob(session_factory,notification_service)
      

    pending_requests_job = PendingRequestsJob(   # 👈 ADD
        session_factory,
        notification_service
    )


    scheduler = SchedulerManager()

    setup_scheduler(
        scheduler,
        work_start_job,
        missing_hours_job,
        open_timer_job,
        contract_expiry_job,
        pending_requests_job,
        start_work_job,
        finish_work_job
    )

    print("STARTING SCHEDULER")
    scheduler.start()

    return scheduler

    #return {

        #"work_start": work_start_job,

       # "missing_hours": missing_hours_job,

        #"open_timer": open_timer_job,

        #"contract_expiry": contract_expiry_job,
        #"pending_requests": pending_requests_job

   # }