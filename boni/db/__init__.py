from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from boni.db.models import __beanie_models__


CLIENT = None
BONIDB = None


async def init(host: str, username: str, password: str, port: int) -> None:
    global CLIENT, BONIDB
    CLIENT = AsyncIOMotorClient(
        host=host, port=port, username=username, password=password
    )
    BONIDB = CLIENT.boni
    await init_beanie(database=BONIDB, document_models=__beanie_models__)
