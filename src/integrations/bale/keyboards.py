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

    return [
        [
            {
                "text": "Approve ✅",
                "callback_data": f"approve_request:{request_id}"
            },
            {
                "text": "Reject ❌",
                "callback_data": f"reject_request:{request_id}"
            }
        ]
    ]