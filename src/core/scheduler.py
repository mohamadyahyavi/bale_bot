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
        hour,
        minute,
        name: str,
        day_of_week: list[str] | None = None,
        
    ):

        if day_of_week is None:
            day_of_week = [
                "sat",
                "sun",
                "mon",
                "tue",
                "wed",
                "thu",
            ]
        
        print("ADDING JOB:", name)
        job = self.scheduler.add_job(
            func,
            trigger=CronTrigger(
                hour=hour,
                minute=minute,
                day_of_week="sat,sun,mon,tue,wed,thu",

            ),
            id=name,
            replace_existing=True,
            coalesce=True,
            max_instances=1
        )

        return job


    def start(self):

        if not self.scheduler.running:

           print("🔥 SCHEDULER STARTED")
           self.scheduler.start()


    def shutdown(self):

        if self.scheduler.running:
            self.scheduler.shutdown()