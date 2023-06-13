from interactions import (
    Extension,
    Client,
)


class RocketLeague(Extension):
    def __init__(self, bot: Client):
        self.bot: Client = bot

    ...


def setup(bot: Client):
    RocketLeague(bot)
