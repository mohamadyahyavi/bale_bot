from fastapi import FastAPI
import httpx
import asyncio

from src.core.config import settings
from src.core.database import get_db
from src.db.session import AsyncSessionLocal

#from src.integrations.bale.bot import bot  # 👈 bot entry point
from src.scheduler.container import build_scheduler_jobs


app = FastAPI()


# -------------------------
# STARTUP
# -------------------------
@app.on_event("startup")
async def startup():

    # -------------------------
    # HTTP CLIENT (for services)
    # -------------------------
    app.state.http_client = httpx.AsyncClient(
        base_url=settings.BALE_API_URL
    )

    # -------------------------
    # DB SESSION (single shared for startup)
    # -------------------------
    #app.state.db = await get_db().__anext__()

    # -------------------------
    # START SCHEDULER
    # -------------------------
    app.state.scheduler = build_scheduler_jobs(
        http_client=app.state.http_client,
        session_factory=AsyncSessionLocal
    )

    # -------------------------
    # START BOT (background task)
    # -------------------------
    #asyncio.create_task(bot.run())


# -------------------------
# SHUTDOWN
# -------------------------
@app.on_event("shutdown")
async def shutdown():

    await app.state.http_client.aclose()

    if hasattr(app.state, "scheduler"):
        app.state.scheduler.shutdown()

    # bot stop if supported
    #try:
      #  await bot.stop()
   ## except:
        #pass