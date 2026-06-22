from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class SchedulerManager:

    def __init__(self):

        self.scheduler = AsyncIOScheduler(
            timezone="Asia/Tehran"
        )


    def add_cron_job(
        self,
        func,
        hour: int,
        minute: int,
        name: str
    ):

        job = self.scheduler.add_job(
            func,
            trigger=CronTrigger(
                hour=hour,
                minute=minute
            ),
            id=name,
            replace_existing=True,
            coalesce=True,
            max_instances=1
        )

        return job


    def start(self):

        if not self.scheduler.running:

           self.scheduler.start()


    def shutdown(self):

        if self.scheduler.running:
            self.scheduler.shutdown()