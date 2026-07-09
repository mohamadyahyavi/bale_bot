from datetime import datetime


class TimeEntryForm:

    STEPS = [
        "project",
        "activity",
        "begin",
        "end",
        "description"
    ]

    QUESTIONS = {

        "project":
            "پروژه را انتخاب کنید:",

        "activity":
            "فعالیت را انتخاب کنید:",

        "begin":
            "⏰ ساعت شروع را وارد کنید.\n\nمثال:\n09:00",

        "end":
            "⏰ ساعت پایان را وارد کنید.\n\nمثال:\n11:30",

        "description":
            "📝 توضیحات کار را وارد کنید:"
    }

    def get_first_step(self):
        return self.STEPS[0]

    def get_next_step(self, current_step):

        index = self.STEPS.index(current_step)

        if index + 1 >= len(self.STEPS):
            return None

        return self.STEPS[index + 1]

    def get_question(self, step):

        return self.QUESTIONS.get(step, step)

    def validate(self, step, value):

        value = value.strip()

        if not value:
            return False

        if step in ["begin", "end"]:

            try:
                datetime.strptime(
                    value,
                    "%H:%M"
                )
                return True

            except ValueError:
                return False

        return True