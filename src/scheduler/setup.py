from src.core.scheduler import SchedulerManager
#from sqlalchemy.ext.asyncio import AsyncSession
from src.jobs.work_start_reminder import WorkStartReminderJob
from src.jobs.missing_hours import MissingHoursJob
from src.jobs.open_timer_check import OpenTimerCheckJob
from src.jobs.contract_expiry import ContractExpiryJob
from src.jobs.pending_requests import PendingRequestsJob
from src.jobs.start_work import WorkStartNotificationJob
from src.jobs.finish_work import WorkEndNotificationJob

def setup_scheduler(
    scheduler: SchedulerManager,
    work_start_job: WorkStartReminderJob,
    missing_hours_job: MissingHoursJob,
    open_timer_job: OpenTimerCheckJob,
    contract_expiry_job: ContractExpiryJob,
    pending_requests_job:PendingRequestsJob,
    start_work_job:WorkStartNotificationJob,
    finish_work_job:WorkEndNotificationJob
):


    # ساعت 10 صبح
    scheduler.add_cron_job(
        func=work_start_job.run,
        hour=10,
        minute=0,
        day_of_week=["mon","tue","wed","thu","sat","sun"],
        name="work_start_reminder"
    )

    scheduler.add_cron_job(
        func=start_work_job.run,
        hour=9,
        minute=0,
        day_of_week=["mon","tue","wed","thu","sat","sun"],
        name="start_work"
    )
    scheduler.add_cron_job(
        func=finish_work_job.run,
        hour=18,
        minute=0,
        day_of_week=["mon","tue","wed","thu","sat","sun"],
        name="finish_work"
    )


    # پایان روز مثلا ساعت 17
    scheduler.add_cron_job(
        func=missing_hours_job.run,
        hour=18,
        minute=30,
        day_of_week=["mon","tue","wed","thu","sat","sun"],
        name="missing_hours"
    )


    # بررسی تایمر باز ساعت 17:30
    scheduler.add_cron_job(
        func=open_timer_job.run,
        hour="*",
        minute="*/1",
        day_of_week=["mon","tue","wed","thu","sat","sun"],
        name="open_timer_check"
    )

    scheduler.add_cron_job(
      func=contract_expiry_job.run,
      hour=10,
      minute=0,
      day_of_week=["mon","tue","wed","thu","sat","sun"],
      name="contract_expiry"
    )

    scheduler.add_cron_job(
    func=pending_requests_job.run,
    hour=12,
    minute=0,
    day_of_week=["mon","tue","wed","thu","sat","sun"],
    name="pending_requests"
)

    