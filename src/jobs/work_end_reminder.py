class WorkEndReminderJob:

    async def run(self):

        users = await self.users.get_active_users()

        for user in users:

            await self.notification.notify_work_end_reminder(
                user.bale_user_id
            )