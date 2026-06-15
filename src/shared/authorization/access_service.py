from src.shared.enums.access_level import AccessLevel

from src.shared.authorization.permission_set import (
    PermissionSet,
)

from src.shared.authorization.policies import (
    employee_permissions,
    manager_permissions,
    hr_permissions,
    ceo_permissions,
    admin_permissions,
)


class AccessService:

    def __init__(self, department_repository):
        self.department_repository = department_repository

    async def is_manager(
        self,
        user_id,
    ) -> bool:
        return await self.department_repository.is_manager(
            user_id
        )

    async def get_permissions(
        self,
        user,
    ) -> PermissionSet:

        permissions = employee_permissions()

        # مدیر دپارتمان؟
        if await self.is_manager(user.id):

            manager_perms = manager_permissions()

            permissions.view_department_users = (
                manager_perms.view_department_users
            )

            permissions.view_department_timesheets = (
                manager_perms.view_department_timesheets
            )

            permissions.approve_department_requests = (
                manager_perms.approve_department_requests
            )

        # HR
        if user.access_level == AccessLevel.HR:

            hr_perms = hr_permissions()

            permissions.view_all_users = (
                hr_perms.view_all_users
            )

            permissions.view_all_timesheets = (
                hr_perms.view_all_timesheets
            )

            permissions.view_all_requests = (
                hr_perms.view_all_requests
            )

        # CEO
        elif user.access_level == AccessLevel.CEO:

            ceo_perms = ceo_permissions()

            permissions.view_all_users = (
                ceo_perms.view_all_users
            )

            permissions.view_all_timesheets = (
                ceo_perms.view_all_timesheets
            )

            permissions.view_all_requests = (
                ceo_perms.view_all_requests
            )

            permissions.view_company_reports = (
                ceo_perms.view_company_reports
            )

        # ADMIN
        elif user.access_level == AccessLevel.ADMIN:

            admin_perms = admin_permissions()

            permissions.manage_users = (
                admin_perms.manage_users
            )

            permissions.manage_departments = (
                admin_perms.manage_departments
            )

            permissions.manage_system = (
                admin_perms.manage_system
            )

        return permissions

    async def can_manage_employee(
        self,
        manager_user,
        employee_user,
    ) -> bool:

        # HR و CEO همه را می‌بینند
        if manager_user.access_level in (
            AccessLevel.HR,
            AccessLevel.CEO,
        ):
            return True

        # مدیر نیست
        if not await self.is_manager(
            manager_user.id
        ):
            return False

        department = (
            await self.department_repository
            .get_by_manager_id(manager_user.id)
        )

        if not department:
            return False

        return (
            employee_user.department_id
            == department.id
        )