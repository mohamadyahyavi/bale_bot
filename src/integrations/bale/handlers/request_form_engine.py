from src.modules.requests.enums import RequestType
from datetime import datetime

class RequestFormEngine:

    FORMS = {

        RequestType.LEAVE.value: {

            "steps": [
                "leave_type",
                "start_datetime",
                "end_datetime",
                "reason"
            ],

            "questions": {

                "leave_type": "Select leave type (DAILY / HOURLY):",

                "start_datetime": 
                    "Enter start datetime(like 2026-06-30 16:00:00):",

                "end_datetime":
                    "Enter end datetime:",

                "reason":
                    "Write reason:"
            }
        },


        RequestType.REMOTE.value: {

            "steps": [
                "date",
                "reason",
                "explanation"
            ],

            "questions": {

                "date":
                    "Enter remote work date:",

                "reason":
                    "Write reason:",
                "explanation":
                    "write details:"    
            }
        },


        RequestType.OVERTIME.value: {

            "steps": [

                "date",
                "hours",
                "reason"
            ],

            "questions": {

                "date":
                    "Enter the date(like 2026-07-02)",

                "hours":
                    "Enter overtime hours(like 3)",

                "reason":
                    "Write reason:"
            }
        },


        RequestType.MISSION.value: {

            "steps": [
                "destination",
                "start_datetime",
                "end_datetime",
                "reason"
            ],

            "questions": {

                "destination":
                    "Enter mission destination:",

                "start_datetime":
                    "Enter start date/time:",

                "end_datetime":
                    "Enter end date/time:",

                "reason":
                    "Write reason:"
            }
        }
    }


    # =========================
    # GET STEPS
    # =========================

    def get_steps(self, request_type: str):

        form = self.FORMS.get(request_type)

        if not form:
            return []

        return form["steps"]



    # =========================
    # GET FIRST STEP
    # =========================

    def get_first_step(self, request_type: str):

        steps = self.get_steps(request_type)

        if not steps:
            return None

        return steps[0]



    # =========================
    # GET NEXT STEP
    # =========================

    def get_next_step(
        self,
        request_type: str,
        current_step: str
    ):

        steps = self.get_steps(request_type)

        if current_step not in steps:
            return None


        index = steps.index(current_step)


        if index + 1 >= len(steps):
            return None


        return steps[index + 1]



    # =========================
    # QUESTION
    # =========================

    def get_question(
        self,
        request_type: str,
        step: str
    ):

        form = self.FORMS.get(request_type)

        if not form:
            return f"Enter {step}"


        return form["questions"].get(
            step,
            f"Enter {step}"
        )



    # =========================
    # FINISHED
    # =========================

    def is_finished(
        self,
        request_type: str,
        current_step: str
    ):

        steps = self.get_steps(request_type)

        if not steps:
            return False


        return steps[-1] == current_step



    # =========================
    # VALIDATION
    # =========================

    def validate(
    self,
    step: str,
    value: str
):

       value = value.strip()

       if not value:
          return False

       if step == "leave_type":
          return value.upper() in [
            "DAILY",
            "HOURLY"
        ]

       if step == "hours":
          return value.isdigit()

       if step in [
          "start_datetime",
          "end_datetime"
        ]:
         try:
            datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S"
            )
            return True
         except ValueError:
            return False

         return True