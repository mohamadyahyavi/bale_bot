from datetime import datetime


class MonthlyReportJob:

    def __init__(self, report_service, notification_service, user_repo):
        self.report = report_service
        self.notification = notification_service
        self.users = user_repo


    async def run(self, month=None, year=None):

        users = await self.users.get_active_users()

        now = datetime.now()

        month = month or now.month
        year = year or now.year

        for user in users:

            report = await self.report.monthly(
                user,
                month,
                year
            )

            message = f"""
📊 گزارش ماهانه

ساعت کارکرد: {report['worked_hours']}
کسری: {report['missing_hours']}
اضافه‌کاری: {report['overtime_hours']}
"""

            await self.notification.send_text(
                user,
                message
            )