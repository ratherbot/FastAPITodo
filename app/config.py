import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")