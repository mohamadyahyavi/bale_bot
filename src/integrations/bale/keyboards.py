from bale.ui.menu_keyboard_markup import MenuKeyboardMarkup
from bale.ui.menu_keyboard_button import MenuKeyboardButton


def request_types_keyboard():
    return {
        "keyboard": [
            ["LEAVE", "REMOTE"],
            ["OVERTIME", "MISSION"],
            ["🔙 بازگشت"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }


def leave_types_keyboard():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton("DAILY"),
        row=1
    )

    keyboard.add(
        MenuKeyboardButton("HOURLY"),
        row=1
    )

    keyboard.add(
        MenuKeyboardButton("SICK"),
        row=2
    )
    keyboard.add(
            MenuKeyboardButton("🔙 بازگشت"),
            row=2
        )

    return keyboard


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


def projects_keyboard(projects):

    keyboard = MenuKeyboardMarkup()

    for project in projects:
        keyboard.add(
            MenuKeyboardButton(
                project["name"]
            )
        )

    keyboard.add(
        MenuKeyboardButton("🔙 بازگشت")
    )

    return keyboard



def activities_keyboard(activities):

    keyboard = MenuKeyboardMarkup()

    for activity in activities:
        keyboard.add(
            MenuKeyboardButton(
                activity["name"]
            )
        )

    keyboard.add(
        MenuKeyboardButton("🔙 بازگشت")
    )

    return keyboard

def team_reports_keyboard():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton("گزارش روزانه تیم")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش هفتگی تیم")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش ماهانه تیم")
    )

    keyboard.add(
        MenuKeyboardButton("🔙 بازگشت")
    )

    return keyboard


def my_reports_keyboard():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton("گزارش روزانه ")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش هفتگی ")
    )

    keyboard.add(
        MenuKeyboardButton("گزارش ماهانه ")
    )

    keyboard.add(
        MenuKeyboardButton("🔙 بازگشت")
    )

    return keyboard


def admin_keyboard():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton("افزودن کاربر جدید"),
        row=1
    )

    keyboard.add(
            MenuKeyboardButton("ثبت ساعت و پروژه"),
            row=1
        )
    
    keyboard.add(
            MenuKeyboardButton("ثبت درخواست جدید"),
            row=2
        )
    keyboard.add(
            MenuKeyboardButton("گزارش های من"),
            row=2
        )
    
    keyboard.add(
            MenuKeyboardButton("مانده مرخصی من"),
            row=3
        )
    keyboard.add(
            MenuKeyboardButton("کارکرد و تاخیر های من"),
            row=3
        )
    
    keyboard.add(
            MenuKeyboardButton("ارسال گزارش اضافه کاری"),
            row=4
        )
    

    return keyboard     

def employee_keyboard():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(
        MenuKeyboardButton("درخواست های من"),
        row=1
    )
    keyboard.add(
        MenuKeyboardButton("ثبت ساعت و پروژه"),
        row=1
    )

    keyboard.add(
        MenuKeyboardButton("ثبت درخواست جدید"),
        row=2
    )
    keyboard.add(
        MenuKeyboardButton("گزارش های من"),
        row=2
    )

    keyboard.add(
        MenuKeyboardButton("مانده مرخصی من"),
        row=3
    )
    keyboard.add(
        MenuKeyboardButton("کارکرد و تاخیر های من"),
        row=3
    )

    keyboard.add(
        MenuKeyboardButton("ارسال گزارش اضافه کاری"),
        row=4
    )

    return keyboard
    



def manager_keyboard():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(MenuKeyboardButton("درخواست های من"), row=1)
    keyboard.add(MenuKeyboardButton("ثبت ساعت و پروژه"), row=1)

    keyboard.add(MenuKeyboardButton("ثبت درخواست جدید"), row=2)
    keyboard.add(MenuKeyboardButton("گزارش های من"), row=2)

    keyboard.add(MenuKeyboardButton("گزارش های تیم"), row=3)
    keyboard.add(MenuKeyboardButton("وضعیت امروز من"), row=3)

    keyboard.add(MenuKeyboardButton("گزارش فعالیت ها"), row=4)
    keyboard.add(MenuKeyboardButton("درخواست های تیم"), row=4)

    keyboard.add(MenuKeyboardButton("مانده مرخصی من"), row=5)
    keyboard.add(MenuKeyboardButton("کارکرد و تاخیر های من"), row=5)

    keyboard.add(MenuKeyboardButton("ارسال گزارش اضافه کاری"), row=6)
    keyboard.add(MenuKeyboardButton("گزارش های اضافه کاری تیم"), row=6)

    return keyboard


def hr_keyboard():

    keyboard = MenuKeyboardMarkup()

    keyboard.add(MenuKeyboardButton("درخواست های من"), row=1)
    keyboard.add(MenuKeyboardButton("ثبت ساعت و پروژه"), row=1)

    keyboard.add(MenuKeyboardButton("ثبت درخواست جدید"), row=2)
    keyboard.add(MenuKeyboardButton("گزارش های من"), row=2)

    keyboard.add(MenuKeyboardButton("همه درخواست های مرخصی"), row=3)
    keyboard.add(MenuKeyboardButton("گزارش منابع انسانی"), row=3)

    keyboard.add(MenuKeyboardButton("مانده مرخصی من"), row=4)
    keyboard.add(MenuKeyboardButton("کارکرد و تاخیر های من"), row=4)

    keyboard.add(MenuKeyboardButton("وضعیت امروز من"), row=5)
    keyboard.add(MenuKeyboardButton("گزارش فعالیت ها"), row=5)
    keyboard.add(MenuKeyboardButton("گزارش های اضافه کاری"), row=6)
    keyboard.add(MenuKeyboardButton("مشاهده لاگ ها"),row=6)


    return keyboard



def ceo_keyboard():

    keyboard = MenuKeyboardMarkup()


    keyboard.add(
        MenuKeyboardButton("درخواست های من")
    )

    keyboard.add(
        MenuKeyboardButton("ثبت ساعت و پروژه")
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

    keyboard.add(
        MenuKeyboardButton("کارکرد و تاخیر های من")
    )

    keyboard.add(
        MenuKeyboardButton("وضعیت امروز من")
    )

    return keyboard