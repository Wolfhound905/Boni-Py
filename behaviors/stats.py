import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from database.statsdb import get_guild_stats
from configuration import get_guilds


guilds = get_guilds()


class clubMatches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    options = [
        {
            "name": "season",
            "description": "Input number of specific season.",
            "type": 4,
            "required": False,
        }
    ]

    @cog_ext.cog_slash(name="stats", options=options, description='Just say /stats to view our current stats!', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, season: int = None):
        get_guild_stats(season)
        
        await ctx.channel.send("placeholder")


def setup(bot):
    bot.add_cog(clubMatches(bot))
