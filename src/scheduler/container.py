from sqlalchemy.ext.asyncio import AsyncSession

from src.integrations.bale.client import BaleClient

from src.integrations.kimai.client import KimaiClient
from src.integrations.kimai.service import KimaiService
from src.modules.requests.repository import RequestRepository
from src.modules.users.repository import UserRepository
from src.jobs.contract_expiry import ContractExpiryJob
from src.modules.notifications.service import NotificationService

from src.modules.reports.service import ReportService
from src.modules.reports.calculator import ReportCalculator

from src.jobs.work_start_reminder import WorkStartReminderJob
from src.jobs.missing_hours import MissingHoursJob
from src.jobs.open_timer_check import OpenTimerCheckJob
from src.jobs.pending_request import PendingRequestsJob
from .setup import setup_scheduler
from src.core.scheduler import SchedulerManager

def build_scheduler_jobs(
    http_client,
    db: AsyncSession
):
    # =========================
    # CLIENTS
    # =========================
    bale_client = BaleClient(
        http_client
    )

    kimai_client = KimaiClient()

    # =========================
    # REPOSITORIES
    # =========================

    user_repository = UserRepository(db)
    request_repository = RequestRepository(db)
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
        kimai_service,
        ReportCalculator()
    )

    # =========================
    # JOBS
    # =========================
    work_start_job = WorkStartReminderJob(
        user_repository,
        report_service,
        notification_service
    )


    missing_hours_job = MissingHoursJob(
        user_repository,
        report_service,
        notification_service
    )


    open_timer_job = OpenTimerCheckJob(
        user_repository,
        report_service,
        notification_service
    )

    contract_expiry_job = ContractExpiryJob(
    user_repository,
    notification_service
)

    pending_requests_job = PendingRequestsJob(   # 👈 ADD
        request_repository,
        user_repository,
        notification_service
    )


    scheduler = SchedulerManager()

    setup_scheduler(
        scheduler,
        work_start_job,
        missing_hours_job,
        open_timer_job,
        contract_expiry_job,
        pending_requests_job
    )

    scheduler.start()

    return scheduler

    #return {

        #"work_start": work_start_job,

       # "missing_hours": missing_hours_job,

        #"open_timer": open_timer_job,

        #"contract_expiry": contract_expiry_job,
        #"pending_requests": pending_requests_job

   # }