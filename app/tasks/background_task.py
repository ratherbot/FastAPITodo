import asyncio
from app.nats.publisher import publish_message
from app.services.currency_parser import get_currency_data
from app.db.database import get_db


async def run_background_task():
    async for db in get_db():
        while True:
            currencies = await get_currency_data(db)
            for currency in currencies:
                await publish_message("currency.updates", currency)
            await asyncio.sleep(60)
