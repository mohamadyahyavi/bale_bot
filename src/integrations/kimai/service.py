from datetime import datetime, time

from .client import KimaiClient


class KimaiService:

    def __init__(self, client: KimaiClient):
        self.client = client

    def _today_range(self):

        now = datetime.now()

        begin = datetime.combine(
            now.date(),
            time.min,
        )

        return begin, now

    async def get_today_timesheets(
        self,
        kimai_user_id: int,
        ):

        begin, end = self._today_range()
        print ("THE FUNCTION GOT CALLED")

        return await self.client.get(
            "/api/timesheets",
            params={
                "user": kimai_user_id,
                "begin": begin.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": end.strftime("%Y-%m-%dT%H:%M:%S"),
            },
        )

    async def has_work_started_today(
        self,
        kimai_user_id: int,
    ) -> bool:

        entries = await self.get_today_timesheets(
            kimai_user_id
        )

        return len(entries) > 0

    async def get_worked_duration(
        self,
        user_id: int,
    ) -> int:

        entries = await self.get_today_timesheets(
            user_id
        )

        return sum(
            entry.get("duration", 0)
            for entry in entries
        )

    async def has_active_timer(
        self,
        kimai_user_id: int,
    ) -> bool:

        entries = await self.client.get(
            "/api/timesheets",
            params={
                "user": kimai_user_id,
                "active": 1,
            },
        )

        return len(entries) > 0

    async def get_active_timers(
        self,
        user_id: int,
    ):

        return await self.client.get(
            "/api/timesheets",
            params={
                "user": user_id,
                "active": 1,
            },
        )

    async def get_open_timesheets(
        self,
        kimai_user_id: int,
    ):

        entries = await self.client.get(
        "/api/timesheets",
        params={
            "user": kimai_user_id,
        },
    )


        return [
            entry
            for entry in entries
            if entry.get("end") is None
        ]

    async def get_today_report(
        self,
        user_id: int,
    ) -> dict:

        entries = await self.get_today_timesheets(
            user_id
        )

        worked_seconds = sum(
            entry.get("duration", 0)
            for entry in entries
        )

        active_timer = any(
            entry.get("end") is None
            for entry in entries
        )

        return {
            "has_entry": len(entries) > 0,
            "worked_seconds": worked_seconds,
            "worked_hours": worked_seconds / 3600,
            "active_timer": active_timer,
            "entries": entries,
        }