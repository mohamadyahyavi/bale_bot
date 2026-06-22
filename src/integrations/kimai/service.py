class KimaiService:

    def __init__(self, client):
        self.client = client


    async def get_user_worklogs(self, user_id, start, end):

        data = await self.client.get_timesheets(
            user_id,
            start,
            end
        )

        logs = []

        for item in data:

            logs.append({
                "project": item["project"]["name"] if item.get("project") else "unknown",
                "duration": item.get("duration", 0),
                "start": item.get("begin"),
                "end": item.get("end")
            })

        return logs


    async def has_open_timer(self, user_id):

        data = await self.client.get_active_timesheets()

        return any(
            item.get("user") == user_id
            for item in data
        )