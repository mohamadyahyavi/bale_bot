from fastapi import APIRouter, Request,Depends
from src.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.integrations.bale.handlers.message_router import MessageRouter

from src.integrations.bale.handlers.request_handler import RequestHandler
from src.integrations.bale.handlers.user_handler import UserHandler
from src.integrations.bale.handlers.report_handler import ReportHandler
from src.integrations.bale.container import build_router

router = APIRouter()


@router.post("/webhook")
async def bale_webhook(request:Request):

    update = await request.json()

    # build fresh router per request (OK for small/medium bot)
    message_router =  request.app.state.message_router

    await message_router.handle(update)

    return {"ok": True}

