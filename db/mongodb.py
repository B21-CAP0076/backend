from motor.motor_asyncio import AsyncIOMotorClient
from odmantic.engine import AIOEngine

from config import settings


async def mongo_engine() -> AIOEngine:
    client = AsyncIOMotorClient(settings.DB_URL)
    engine = AIOEngine(motor_client=client, database=settings.DB_NAME)
    return engine
