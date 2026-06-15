from fastapi import APIRouter, Request
from src.integrations.bale.handlers.message_router import MessageRouter

router = APIRouter()

message_router = MessageRouter()

@router.post("/webhook")
async def bale_webhook(request: Request):

    update = await request.json()

    await message_router.handle(update)

    return {"ok": True}