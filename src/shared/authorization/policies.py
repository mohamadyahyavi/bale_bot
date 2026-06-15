from src.shared.authorization.permission_set import (
    PermissionSet,
)


def employee_permissions():

    return PermissionSet(
        view_self_timesheet=True,
        view_own_requests=True,
        submit_leave_request=True,
        submit_remote_request=True,
    )


def manager_permissions():

    permissions = employee_permissions()

    permissions.view_department_users = True

    permissions.view_department_timesheets = True

    permissions.approve_department_requests = True

    return permissions


def hr_permissions():

    permissions = employee_permissions()

    permissions.view_all_users = True
    permissions.view_all_timesheets = True
    permissions.view_all_requests = True

    return permissions


def ceo_permissions():

    permissions = employee_permissions()

    permissions.view_all_users = True
    permissions.view_all_timesheets = True
    permissions.view_all_requests = True

    permissions.view_company_reports = True

    return permissions


def admin_permissions():

    permissions = employee_permissions()

    permissions.manage_users = True
    permissions.manage_departments = True
    permissions.manage_system = True

    return permissions