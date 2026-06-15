from dataclasses import dataclass,fields


@dataclass(slots=True)
class PermissionSet:

    view_self_timesheet: bool = False
    view_own_requests: bool = False

    submit_leave_request: bool = False
    submit_remote_request: bool = False

    view_department_users: bool = False
    view_department_timesheets: bool = False

    approve_department_requests: bool = False

    view_all_users: bool = False
    view_all_timesheets: bool = False
    view_all_requests: bool = False

    view_company_reports: bool = False

    manage_users: bool = False
    manage_departments: bool = False
    manage_system: bool = False
    def merge(self, other: "PermissionSet"):

        for field in fields(self):

            if getattr(other, field.name):
                setattr(
                    self,
                    field.name,
                    True,
                )