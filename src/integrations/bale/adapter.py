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

        if hasattr(self.update, "text"):

            user = self.update.from_user

            result["message"] = {
                "text": self.update.text or "",

                "from": {
                    "id": str(user.id) if user else ""
                }
            }

        # -------------------------
        # CALLBACK QUERY
        # -------------------------
        #callback = getattr(self.update, "callback_query", None)

        elif hasattr(self.update, "data"):

            user = self.update.from_user

            result["callback_query"] = {

                "data": self.update.data or "",

                "from": {
                    "id": str(user.id) if user else ""
                }
            }


        return result