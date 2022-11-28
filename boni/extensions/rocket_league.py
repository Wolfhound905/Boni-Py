import naff

class RocketLeague(naff.Extension):
    def __init__(self, bot: naff.Client):
        self.bot: naff.Client = bot

    ...


def setup(bot: naff.Client):
    RocketLeague(bot)
