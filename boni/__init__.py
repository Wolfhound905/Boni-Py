import naff
from dotenv import get_key

from boni.db import init
from boni.utils import get_extensions

if debug_scope := get_key(".env", "DEBUG_SCOPE"):
    boni = naff.Client(
        intents=naff.Intents.MESSAGES | naff.Intents.DEFAULT,
        sync_interactions=True,
        debug_scope=int(debug_scope),
        delete_unused_application_cmds=True,
    )
else:
    boni = naff.Client(
        intents=naff.Intents.MESSAGES | naff.Intents.DEFAULT,
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
    for extension in get_extensions("./boni/extensions/"):
        boni.load_extension(extension)

    await boni.astart(get_key(".env", "TOKEN"))
