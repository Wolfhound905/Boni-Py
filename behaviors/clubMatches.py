import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import random

class clubMatches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    options = [
        {
            "name":"win",
            "description":"Report a club win )",
            "required":False,
            "type":0
        },
        {
            "name":"loss",
            "description":"Report a club loss :(",
            "required":False,
            "type":0
        }
    ]

    @cog_ext.cog_subcommand(base="club", name="match", description="Let me know wether you won or loss.", options= options, guild_ids = [443884809484238848])
    async def group_say(self, ctx: SlashContext):
        await ctx.send("placeholder")

def setup(bot):
    bot.add_cog(clubMatches(bot))
