def request_types_keyboard():
    return {
        "keyboard": [
            ["LEAVE", "REMOTE"],
            ["OVERTIME", "MISSION"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }

def approval_keyboard(request_id):

    return {
        "keyboard": [
            [
                f"APPROVE:{request_id}",
                f"REJECT:{request_id}"
            ]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }