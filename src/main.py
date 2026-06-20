from fastapi import FastAPI
import httpx
from src.integrations.bale.container import build_router
from src.integrations.bale.webhook import router
from src.core.config import settings

app = FastAPI()
app.include_router(router)
#print("MAIN RUNNING",__file__)
#print ("working:",os.getcwd())
#print ("Routes:",app.routes)



@app.on_event("startup")
async def startup():
    app.state.http_client = httpx.AsyncClient(
        base_url=f"{settings.BALE_API_URL}{settings.BALE_BOT_TOKEN}"
    )
    


@app.on_event("shutdown")
async def shutdown():
    await app.state.http_client.aclose()