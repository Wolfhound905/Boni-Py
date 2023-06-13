from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from boni.db.models import __beanie_models__


async def init(host: str, database: str, port: int = 27017, user: str = None, password: str = None, models: list = None):
    client = AsyncIOMotorClient(username=user, password=password, host=host, port=port)
    await init_beanie(database=client[database], document_models=models or __beanie_models__)
