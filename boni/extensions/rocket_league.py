import asyncio
import naff
from datetime import timedelta

from boni.utils.rocket_league import Tournament, get_tourneys


class RocketLeague(naff.Extension):
    def __init__(self, bot: naff.Client):
        self.bot: naff.Client = bot

    ...


def setup(bot: naff.Client):
    RocketLeague(bot)
