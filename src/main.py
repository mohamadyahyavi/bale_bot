from fastapi import FastAPI
import httpx

from src.core.config import settings

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.http_client = httpx.AsyncClient(
        base_url=f"{settings.BALE_API_URL}{settings.BALE_BOT_TOKEN}"
    )


@app.on_event("shutdown")
async def shutdown():
    await app.state.http_client.aclose()