from src.modules.requests.enums import RequestType


class RequestFormEngine:

    FORMS = {
        RequestType.LEAVE.value: [
            "leave_type",      # DAILY / HOURLY
            "start_datetime",
            "end_datetime",
            "reason"
        ],

        RequestType.REMOTE.value: [
            "date",
            "reason"
        ],

        RequestType.OVERTIME.value: [
            "hours",
            "reason"
        ],

        RequestType.MISSION.value: [
            "destination",
            "start_datetime",
            "end_datetime",
            "reason"
        ],
    }

    # -------------------------
    # GET FIRST STEP
    # -------------------------
    def get_first_step(self, request_type: str):
        return self.FORMS[request_type][0]

    # -------------------------
    # GET NEXT STEP
    # -------------------------
    def get_next_step(self, request_type: str, current_step: str):

        steps = self.FORMS.get(request_type, [])

        if current_step not in steps:
            return None

        index = steps.index(current_step)

        if index + 1 >= len(steps):
            return None

        return steps[index + 1]

    # -------------------------
    # CHECK FINISH
    # -------------------------
    def is_finished(self, request_type: str, current_step: str):

        steps = self.FORMS.get(request_type, [])

        return steps and steps[-1] == current_step

    # -------------------------
    # SIMPLE VALIDATION
    # -------------------------
    def validate(self, step: str, value: str) -> bool:

        if step in ["start_datetime", "end_datetime"]:
            return len(value) > 5

        if step == "hours":
            return value.isdigit()

        if step == "leave_type":
            return value in ["DAILY", "HOURLY"]

        return len(value.strip()) > 0