import httpx


class KimaiClient:

    def __init__(
        self,
        base_url: str,
        token: str
    ):

        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )


    async def get_timesheets(
        self,
        user_id: int,
        start: str,
        end: str
    ):

        response = await self.client.get(
            "/api/timesheets",
            params={
                "user": user_id,
                "begin": start,
                "end": end
            }
        )


        response.raise_for_status()

        return response.json()



    async def get_active_timesheets(
        self,
        user_id: int | None = None
    ):

        params = {
            "active": 1
        }


        if user_id:
            params["user"] = user_id


        response = await self.client.get(
            "/api/timesheets",
            params=params
        )


        response.raise_for_status()

        return response.json()