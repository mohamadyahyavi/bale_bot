from enum import StrEnum


class Permission(StrEnum):

    # employee
    VIEW_SELF_TIMESHEET = "view_self_timesheet"
    VIEW_OWN_REQUESTS = "view_own_requests"

    SUBMIT_LEAVE_REQUEST = "submit_leave_request"
    SUBMIT_REMOTE_REQUEST = "submit_remote_request"

    # manager
    VIEW_DEPARTMENT_USERS = "view_department_users"
    VIEW_DEPARTMENT_TIMESHEETS = "view_department_timesheets"

    APPROVE_DEPARTMENT_REQUESTS = (
        "approve_department_requests"
    )

    # hr
    VIEW_ALL_USERS = "view_all_users"
    VIEW_ALL_TIMESHEETS = "view_all_timesheets"
    VIEW_ALL_REQUESTS = "view_all_requests"

    # ceo
    VIEW_COMPANY_REPORTS = "view_company_reports"

    # admin
    MANAGE_USERS = "manage_users"
    MANAGE_DEPARTMENTS = "manage_departments"
    MANAGE_SYSTEM = "manage_system"