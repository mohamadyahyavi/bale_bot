import asyncio

from bale import Bot,Message

from src.core.config import settings
from src.integrations.bale.adapter import BaleUpdateAdapter
from src.integrations.bale.container import build_router
from src.core.database import get_db
import httpx

#handle
bot = Bot(settings.BALE_BOT_TOKEN)

http_client = httpx.AsyncClient(
    base_url=settings.BALE_API_URL
)


@bot.event
async def on_message(update:Message):

    await update.reply(update.content)

    adapter = BaleUpdateAdapter(update)
    data = adapter.to_dict()

    async for db in get_db():

        router = build_router(
            http_client,
            db
        )

        await router.handle(data)

        break
@bot.event
async def on_callback(callback):

    adapter = BaleUpdateAdapter(callback)

    data = adapter.to_dict()

    async for db in get_db():

        router = build_router(
            http_client,
            db
        )

        await router.handle(data)

        break    

if __name__ == "__main__":

   bot.run()
    