import httpx
from src.core.config import settings


class BaleClient:

    def __init__(self, http_client: httpx.AsyncClient):
        self.http = http_client


    async def send_message(self, chat_id: str, text: str, keyboard=None):

        url = f"/bot{settings.BALE_BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text
        }

        if keyboard:

    # python-bale-bot object
           if hasattr(keyboard, "to_dict"):
              payload["reply_markup"] = keyboard.to_dict()

    # already dict
           elif isinstance(keyboard, dict):
             payload["reply_markup"] = keyboard


        print("URL:", self.http.base_url, url)
        print("PAYLOAD:", payload)


        response = await self.http.post(
          url,
          json=payload,
          timeout=10
           )


        print("STATUS:", response.status_code)
        print("BODY:", response.text)


        response.raise_for_status()

        return response.json()
    
    async def send_document(
    self,
    chat_id: str,
    file_id: str,
    caption: str = None
):

      url = f"/bot{settings.BALE_BOT_TOKEN}/sendDocument"

      payload = {
        "chat_id": chat_id,
        "document": file_id
    }

      if caption:
        payload["caption"] = caption


      print("DOCUMENT URL:", self.http.base_url, url)
      print("DOCUMENT PAYLOAD:", payload)


      response = await self.http.post(
        url,
        json=payload,
        timeout=10
    )


      print("STATUS:", response.status_code)
      print("BODY:", response.text)


      response.raise_for_status()

      return response.json()
    
    async def edit_message(
    self,
    chat_id: str,
    message_id: int,
    text: str,
    keyboard=None
):

        url = f"/bot{settings.BALE_BOT_TOKEN}/editMessageText"


        payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
        }


        if keyboard:
           if hasattr(keyboard, "to_dict"):
              payload["reply_markup"] = keyboard.to_dict()

           elif isinstance(keyboard, dict):
              payload["reply_markup"] = keyboard


        print("EDIT URL:", self.http.base_url, url)
        print("EDIT PAYLOAD:", payload)


        response = await self.http.post(
           url,
           json=payload,
           timeout=10
        )


        print("STATUS:", response.status_code)
        print("BODY:", response.text)


        response.raise_for_status()

        return response.json()
       

    async def delete_message(
        self,
        chat_id: str,
        message_id: int
    ):

        url = f"/bot{settings.BALE_BOT_TOKEN}/deleteMessage"


        payload = {
            "chat_id": chat_id,
            "message_id": message_id
        }


        print("DELETE URL:", self.http.base_url, url)
        print("DELETE PAYLOAD:", payload)



        response = await self.http.post(
            url,
            json=payload,
            timeout=10
        )


        print("DELETE STATUS:", response.status_code)
        print("DELETE BODY:", response.text)


        response.raise_for_status()

        return response.json()   