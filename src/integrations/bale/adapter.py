# src/integrations/bale/adapter.py


class BaleUpdateAdapter:
    """
    تبدیل update های python-bale-bot به فرمت dict
    که MessageRouter فعلی بدون هیچ تغییری کار کند
    """

    def __init__(self, update):
        self.update = update

    def to_dict(self):
        result = {}

        # -------------------------
        # MESSAGE
        # -------------------------
        #message = getattr(self.update, "message", None)

        if hasattr(self.update, "text") or getattr(self.update, "document", None):

            user = self.update.from_user

            message = {
                "text": self.update.text or "",
                "from": {
                    "id": str(user.id) if user else ""
                }
            }

            # Document
            if getattr(self.update, "document", None):

                doc = self.update.document

                message["document"] = {
                    "file_id": doc.file_id,
                    "file_name": doc.file_name,
                    "file_size": doc.file_size,
                    "mime_type": getattr(doc, "mime_type", None)
                }

            # ---------- Photo ----------
            if getattr(self.update, "photos", None):

                photos = self.update.photos

                if photos:
                    photo = photos[-1]

                    message["photo"] = {
                        "file_id": photo.file_id
                    }

            result["message"] = message    

        # -------------------------
        # CALLBACK
        # -------------------------
        elif hasattr(self.update, "data"):

            print(type(self.update))
            print(self.update)
            print(dir(self.update))

            user = self.update.from_user

            result["callback_query"] = {
                "data": self.update.data or "",
                "from": {
                    "id": str(user.id) if user else ""
                }
            }

        return result