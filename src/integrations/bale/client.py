import http

class BaleClient:

    def __init__(self, http_client:http):
        self.http = http_client

    async def send_message(self, chat_id: str, text: str, keyboard=None):
        payload = {
            "chat_id": chat_id,
            "text": text
            
        }

        if keyboard:

            payload["reply_markup"] = keyboard

        response = await self.http.post("/sendMessage", json=payload)

        return response.json()