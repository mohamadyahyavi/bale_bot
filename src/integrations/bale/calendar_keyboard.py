import calendar
from datetime import datetime

from bale.ui.inline_keyboard_markup import InlineKeyboardMarkup
from bale.ui.inline_keyboard_button import InlineKeyboardButton


MONTH_NAMES = [
    "",
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

WEEK_DAYS = [
    "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"
]


def leave_calendar_keyboard(
    year: int | None = None,
    month: int | None = None,
):

    now = datetime.now()

    if year is None:
        year = now.year

    if month is None:
        month = now.month

    keyboard = InlineKeyboardMarkup()

    # =========================
    # Header
    # =========================

    keyboard.add(
        InlineKeyboardButton(
            "◀",
            callback_data=f"cal_prev:{year}:{month}"
        ),
        row=1
    )

    keyboard.add(
        InlineKeyboardButton(
            f"{MONTH_NAMES[month]} {year}",
            callback_data="ignore"
        ),
        row=1
    )

    keyboard.add(
        InlineKeyboardButton(
            "▶",
            callback_data=f"cal_next:{year}:{month}"
        ),
        row=1
    )

    # =========================
    # Week names
    # =========================

    for day in WEEK_DAYS:

        keyboard.add(
            InlineKeyboardButton(
                day,
                callback_data="ignore"
            ),
            row=2
        )

    # =========================
    # Month days
    # =========================

    month_calendar = calendar.monthcalendar(year, month)

    row_number = 3

    for week in month_calendar:

        for day in week:

            if day == 0:

                keyboard.add(
                    InlineKeyboardButton(
                        " ",
                        callback_data="ignore"
                    ),
                    row=row_number
                )

            else:

                keyboard.add(
                    InlineKeyboardButton(
                        str(day),
                        callback_data=f"cal_day:{year}:{month}:{day}"
                    ),
                    row=row_number
                )

        row_number += 1

    return keyboard


def previous_month(year: int, month: int):

    if month == 1:
        return year - 1, 12

    return year, month - 1


def next_month(year: int, month: int):

    if month == 12:
        return year + 1, 1

    return year, month + 1