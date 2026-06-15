class PermissionService:

    def __init__(self, access_control):
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

        context = await self.get_context(user_id)

        # همه اجازه دارند درخواست ثبت کنند
        return True


    async def can_view_own_requests(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return context["role"] in ["EMPLOYEE", "HR", "CEO"]


    async def can_view_all_requests(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return context["role"] in ["HR", "CEO"]


    async def can_view_department_requests(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return (
            context["role"] in ["HR", "CEO"]
            or context["is_manager"] is True
        )


    async def can_approve_request(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return (
            context["role"] in ["HR", "CEO"]
            or context["is_manager"] is True
        )

    # -------------------------
    # REPORT PERMISSIONS
    # -------------------------

    async def can_view_own_reports(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return context["role"] in ["EMPLOYEE", "HR", "CEO", "MANAGER"]


    async def can_view_team_reports(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return (
            context["role"] in ["HR", "CEO"]
            or context["is_manager"] is True
        )


    async def can_view_all_reports(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return context["role"] in ["HR", "CEO"]

    # -------------------------
    # NOTIFICATION PERMISSIONS
    # -------------------------

    async def can_receive_hr_notifications(self, user_id: str) -> bool:

        context = await self.get_context(user_id)

        return context["role"] in ["HR", "CEO"]