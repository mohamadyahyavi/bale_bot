from src.core.scheduler import SchedulerManager
#from sqlalchemy.ext.asyncio import AsyncSession
from src.jobs.work_start_reminder import WorkStartReminderJob
from src.jobs.missing_hours import MissingHoursJob
from src.jobs.open_timer_check import OpenTimerCheckJob
from src.jobs.contract_expiry import ContractExpiryJob
from src.jobs.pending_request import PendingRequestsJob


def setup_scheduler(
    scheduler: SchedulerManager,
    work_start_job: WorkStartReminderJob,
    missing_hours_job: MissingHoursJob,
    open_timer_job: OpenTimerCheckJob,
    contract_expiry_job: ContractExpiryJob,
    pending_requests_job:PendingRequestsJob
):


    # ساعت 10 صبح
    scheduler.add_cron_job(
        func=work_start_job.run,
        hour=10,
        minute=0,
        name="work_start_reminder"
    )


    # پایان روز مثلا ساعت 17
    scheduler.add_cron_job(
        func=missing_hours_job.run,
        hour=17,
        minute=30,
        name="missing_hours"
    )


    # بررسی تایمر باز ساعت 17:30
    scheduler.add_cron_job(
        func=open_timer_job.run,
        hour=17,
        minute=30,
        name="open_timer_check"
    )

    scheduler.add_cron_job(
      func=contract_expiry_job.run,
      hour=9,
      minute=0,
      name="contract_expiry"
    )

    scheduler.add_cron_job(
    func=pending_requests_job.run,
    hour=13,
    minute=0,
    name="pending_requests"
)

    