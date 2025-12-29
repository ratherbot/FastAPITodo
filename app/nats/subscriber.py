import asyncio
from nats.aio.client import Client as NATS
from app.config import NATS_URL


async def subscribe_to_channel(subject: str):
    nc = NATS()

    try:
        await nc.connect(NATS_URL)

        async def message_handler(msg):
            print(f"Received message: {msg.data.decode()}")

        await nc.subscribe(subject, cb=message_handler)
        await asyncio.Event().wait()
    finally:
        await nc.close()


asyncio.run(subscribe_to_channel("currency.updates"))