from .access_control import AccessControlService


class PermissionService:

    def __init__(self, access_control: AccessControlService):
        self.access_control = access_control


    # -------------------------
    # CONTEXT
    # -------------------------

    async def get_context(self, user_id: str):
        return await self.access_control.get_context(user_id)


    # -------------------------
    # REQUEST PERMISSIONS
    # -------------------------

    async def can_create_request(self, user_id: str) -> bool:
        return True


    async def can_view_own_requests(self, user_id: str) -> bool:
        return True


    async def can_view_all_requests(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return context["role"] in ["HR", "CEO"]


    async def can_view_department_requests(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return context["is_manager"]


    async def can_approve_request(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return context["is_manager"]


    # -------------------------
    # REPORT PERMISSIONS
    # -------------------------

    async def can_view_own_reports(self, user_id: str) -> bool:
        return True


    async def can_view_team_reports(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return (
            context["is_manager"]
            or context["role"] in ["HR", "CEO"]
        )


    async def can_view_all_reports(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return context["role"] in ["HR", "CEO"]


    # -------------------------
    # NOTIFICATIONS
    # -------------------------

    async def can_receive_hr_notifications(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return context["role"] in ["HR", "CEO"]


    # -------------------------
    # AGGREGATION
    # -------------------------

    async def get_permissions(self, user_id: str):

        return {
            "can_create_request": await self.can_create_request(user_id),
            "can_view_own_requests": await self.can_view_own_requests(user_id),
            "can_view_all_requests": await self.can_view_all_requests(user_id),
            "can_view_department_requests": await self.can_view_department_requests(user_id),
            "can_approve_request": await self.can_approve_request(user_id),
            "can_view_own_reports": await self.can_view_own_reports(user_id),
            "can_view_team_reports": await self.can_view_team_reports(user_id),
            "can_view_all_reports": await self.can_view_all_reports(user_id),
            "can_receive_hr_notifications": await self.can_receive_hr_notifications(user_id),
        }