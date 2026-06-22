from fastapi import FastAPI
import httpx
from src.core.database import get_db
from src.integrations.bale.container import build_router
from src.integrations.bale.webhook import router
from src.core.config import settings
from src.core.scheduler import SchedulerManager
from src.scheduler.setup import setup_scheduler
from src.scheduler.container import build_scheduler_jobs


app = FastAPI()
app.include_router(router)
#print("MAIN RUNNING",__file__)
#print ("working:",os.getcwd())
#print ("Routes:",app.routes)



@app.on_event("startup")
async def startup():
    app.state.http_client = httpx.AsyncClient(
        base_url=settings.BALE_API_URL
    )

    app.state.db = await get_db().__anext__()

    app.state.message_router = build_router(
        app.state.http_client,
        app.state.db
    )

    app.state.scheduler = build_scheduler_jobs(
        http_client=app.state.http_client,
        db=app.state.db
    )
    


@app.on_event("shutdown")
async def shutdown():
    await app.state.http_client.aclose()
    if hasattr(app.state, "scheduler"):
        app.state.scheduler.shutdown()