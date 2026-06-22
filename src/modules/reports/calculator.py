class ReportCalculator:

    REQUIRED_HOURS = 7


    def worked_hours(self, timesheet):

        total_seconds = sum(
            x["duration"] for x in timesheet
        )

        return total_seconds / 3600


    def missing_hours(self, worked):

        return max(self.REQUIRED_HOURS - worked, 0)


    def overtime_hours(self, worked):

        return max(worked - self.REQUIRED_HOURS, 0)