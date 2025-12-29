import asyncio
import json
from nats.aio.client import Client as NATS
from app.config import NATS_URL


async def publish_message(subject: str, message: dict):
    nc = NATS()

    await nc.connect(NATS_URL)
    await nc.publish(subject, json.dumps(message).encode())
    await nc.flush()
    await nc.close()


async def publish_unique_message(subject: str):
    unique_message = {"task": "background_task", "status": "started"}
    await publish_message(subject, unique_message)