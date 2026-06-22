import httpx
from src.core.config import settings

class BaleClient:

    def __init__(self, http_client:httpx.AsyncClient,token:str):
        self.http = http_client
        self.token = token
        
    async def send_message(self, chat_id: str, text: str, keyboard=None):
        url = f"/bot{self.token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
            
        }

        if keyboard:

            payload["reply_markup"] = keyboard

        response = await self.http.post(url, json=payload,timeout=10)

        response.raise_for_status()

        return response.json()