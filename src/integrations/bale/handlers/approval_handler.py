class ApprovalHandler:

    def __init__(self, request_service, bale_client):
        self.request_service = request_service
        self.bale = bale_client

    async def handle_approve(self, update: dict):

        callback = update.get("callback_query", {})
        manager_id = callback["from"]["id"]
        request_id = callback["data"].split(":")[1]

        request = await self.request_service.approve_request(
            request_id=request_id,
            manager_id=manager_id
        )

        return await self.bale.send_message(
            manager_id,
            "Request approved ✔️"
        )

    async def handle_reject(self, update: dict):

        callback = update.get("callback_query", {})
        manager_id = callback["from"]["id"]
        request_id = callback["data"].split(":")[1]

        await self.request_service.reject_request(
            request_id=request_id,
            manager_id=manager_id
        )

        return await self.bale.send_message(
            manager_id,
            "Request rejected ❌"
        )