import dis_snek as dis
from dotenv import get_key

from boni.db import init
from boni.utils import get_cogs

if debug_scope := get_key(".env", "DEBUG_SCOPE"):
    boni = dis.Snake(
        intents=dis.Intents.MESSAGES | dis.Intents.DEFAULT,
        sync_interactions=True,
        debug_scope=int(debug_scope),
        delete_unused_application_cmds=True,
    )
else:
    boni = dis.Snake(
        intents=dis.Intents.MESSAGES | dis.Intents.DEFAULT,
        sync_interactions=True,
        delete_unused_application_cmds=False,  # this is a bit buggy on restarts
    )


async def run() -> None:
    await init(
        host=get_key(".env", "HOST"),
        username=get_key(".env", "USERNAME"),
        password=get_key(".env", "PASSWORD"),
        port=int(get_key(".env", "PORT")),
    )
    for scale in get_cogs("./boni/cogs/"):
        boni.grow_scale(scale)

    await boni.astart(get_key(".env", "TOKEN"))
