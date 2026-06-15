class UserHandler:

    def __init__(self, user_service, bale_client):
        self.user_service = user_service
        self.bale = bale_client

    async def handle_start(self, bale_user_id: str):

        user = await self.user_service.get_by_bale_id(bale_user_id)

        if not user:
            return await self.bale.send_message(
                bale_user_id,
                "User not registered"
            )

        menu = self._build_menu(user)

        return await self.bale.send_message(
            bale_user_id,
            f"Welcome {user.first_name}",
            keyboard=menu
        )

    def _build_menu(self, user):

        if user.access_level == "HR":
            return ["Requests", "Reports", "All Users"]

        if user.access_level == "CEO":
            return ["Reports", "All Requests"]

        # Employee / Manager
        return ["Create Request", "My Requests", "My Reports"]