from typing import Any
from src.core.config import settings

import httpx


class KimaiClient:
    def __init__(
        self,
        base_url: str,
        token: str,
    ):
        self.base_url = base_url.rstrip("/")

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        self.timeout = 20.0

    async def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ) -> Any:

        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
        ) as client:

            response = await client.get(
                endpoint,
                params=params,
            )

            print("URL:", response.request.url)
            print("STATUS:", response.status_code)
            print(settings.KIMAI_BASE_URL)
            print(settings.KIMAI_USERNAME)
            print(settings.KIMAI_API_TOKEN)
            if response.status_code != 200:
                print("BODY:", response.text)

            response.raise_for_status()

            return response.json()
        
    async def post(
       self,
       endpoint: str,
       json: dict,
       ):

       async with httpx.AsyncClient(
        base_url=self.base_url,
        headers=self.headers,
        timeout=self.timeout,
       ) as client:

            response = await client.post(
            endpoint,
            json=json,
            )

            print("URL:", response.request.url)
            print("STATUS:", response.status_code)

            if response.status_code not in (200, 201):
               print("BODY:", response.text)

            response.raise_for_status()

            return response.json()