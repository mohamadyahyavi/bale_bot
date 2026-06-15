from integrations.bale.constants.steps import Steps


class RequestFlow:

    def __init__(self, state):
        self.state = state

    # ---------- LEAVE ----------

    async def start_leave(self, user_id):

        self.state.set(user_id, "step", Steps.LEAVE_TYPE)

        return "نوع مرخصی را وارد کنید"


    async def leave_type(self, user_id, text):

        self.state.set(user_id, "leave_type", text)
        self.state.set(user_id, "step", Steps.LEAVE_DATES)

        return "از تاریخ و تا تاریخ را وارد کنید (YYYY-MM-DD YYYY-MM-DD)"


    async def leave_dates(self, user_id, text, usecase):

        start_date, end_date = text.split(" ")

        leave_type = self.state.get(user_id, "leave_type")


        result = await usecase.execute(
            user_id,
            {
                "type": "LEAVE",
                "data": {
                    "start_date": start_date,
                    "end_date": end_date,
                    "leave_type": leave_type
                }
            }
        )


        self.state.clear(user_id)

        return f"مرخصی ثبت شد ✅ ({result.id})"


    # ---------- MISSION ----------

    async def start_mission(self, user_id):

        self.state.set(user_id, "step", Steps.MISSION_LOCATION)

        return "مکان ماموریت را وارد کنید"


    async def mission_location(self, user_id, text):

        self.state.set(user_id, "location", text)
        self.state.set(user_id, "step", Steps.MISSION_DATES)

        return "بازه زمانی (start end)"


    async def mission_dates(self, user_id, text):

        start_date, end_date = text.split(" ")

        self.state.set(user_id, "start_date", start_date)
        self.state.set(user_id, "end_date", end_date)
        self.state.set(user_id, "step", Steps.MISSION_DESCRIPTION)

        return "توضیحات ماموریت را وارد کنید"


    async def mission_description(self, user_id, text, usecase):

        location = self.state.get(user_id, "location")
        start_date = self.state.get(user_id, "start_date")
        end_date = self.state.get(user_id, "end_date")


        result = await usecase.execute(
            user_id,
            {
                "type": "MISSION",
                "data": {
                    "location": location,
                    "start_date": start_date,
                    "end_date": end_date,
                    "description": text
                }
            }
        )


        self.state.clear(user_id)

        return f"ماموریت ثبت شد ✅ ({result.id})"