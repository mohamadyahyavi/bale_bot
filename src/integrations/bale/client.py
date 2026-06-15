class BaleClient:

    def __init__(self, http_client):
        self.http = http_client

    async def send_message(self, chat_id: str, text: str, keyboard=None):
        payload = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": keyboard
        }

        await self.http.post("/sendMessage", json=payload)