from interactions import (
    MISSING,
    Client,
    Intents,
)
from dotenv import get_key

from boni.db import init
from boni.utils import get_extensions
from boni.utils.config import load_config


async def run() -> None:
    config = load_config()

    await init(
        host=config.mongodb.host,
        database=config.mongodb.database,
        user=config.mongodb.username,
        password=config.mongodb.password,
    )

    boni = Client(
        intents=Intents.MESSAGES | Intents.DEFAULT,
        sync_interactions=True,
        debug_scope=config.discord.debug_scope or MISSING,
        send_command_tracebacks=True if config.discord.debug_scope else False,
        delete_unused_application_cmds=True,
    )

    for extension in get_extensions("./boni/extensions/"):
        boni.load_extension(extension)

    await boni.astart(config.discord.token)
