from bale.ui.menu_keyboard_markup import MenuKeyboardMarkup
from bale.ui.menu_keyboard_button import MenuKeyboardButton


def request_types_keyboard():
    return {
        "keyboard": [
            ["LEAVE", "REMOTE"],
            ["OVERTIME", "MISSION"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }


def request_action_keyboard(request_id):

    return {
        "inline_keyboard": [
            [
                {
                    "text": "Approve ✅",
                    "callback_data": f"approve_request:{str(request_id)}"
                },
                {
                    "text": "Reject ❌",
                    "callback_data": f"reject_request:{str(request_id)}"
                }
            ]
        ]
    }


def my_reports_keyboard():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton("گزارش روزانه")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش هفتگی")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش ماهانه")
    )

    keyboard.add(
        MenuKeyboardButton("🔙 بازگشت")
    )

    return keyboard

def employee_keyboard():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton("درخواست های من")
    )

    keyboard.add(
        MenuKeyboardButton("ثبت ساعت")
    )

    keyboard.add(
        MenuKeyboardButton("ثبت درخواست جدید")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش های من")
    )

    keyboard.add(
        MenuKeyboardButton("مانده مرخصی من")
    )

    return keyboard



def manager_keyboard():

    keyboard = MenuKeyboardMarkup()


    # منوی کارمند
    keyboard.add(
        MenuKeyboardButton("درخواست های من")
    )

    keyboard.add(
        MenuKeyboardButton("ثبت ساعت")
    )

    keyboard.add(
        MenuKeyboardButton("ثبت درخواست جدید")
    )

    keyboard.add(
        MenuKeyboardButton("درخواست های تیم")
    )

    keyboard.add(
        MenuKeyboardButton(" مانده مرخصی من")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش های تیم")
    )


    return keyboard



def hr_keyboard():

    keyboard = MenuKeyboardMarkup()


    keyboard.add(
        MenuKeyboardButton("درخواست های من")
    )

    keyboard.add(
        MenuKeyboardButton("ثبت ساعت")
    )

    keyboard.add(
        MenuKeyboardButton("ثبت درخواست جدید")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش های من")
    )


    keyboard.add(
        MenuKeyboardButton("همه درخواست های مرخصی")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش همه")
    )
    keyboard.add(
        MenuKeyboardButton("مانده مرخصی من")
    )


    return keyboard



def ceo_keyboard():

    keyboard = MenuKeyboardMarkup()


    keyboard.add(
        MenuKeyboardButton("درخواست های من")
    )

    keyboard.add(
        MenuKeyboardButton("ثبت ساعت")
    )

    keyboard.add(
        MenuKeyboardButton("ثبت درخواست جدید")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش های من")
    )


    keyboard.add(
        MenuKeyboardButton("همه درخواست ها")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش همه")
    )


    return keyboard