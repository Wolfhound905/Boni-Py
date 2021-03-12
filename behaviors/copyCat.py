import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class copyCat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="say", description='Enter a message and I will repeat it :)', guild_ids = [443884809484238848])
    async def group_say(self, ctx: SlashContext, message: str):
        await ctx.send(message)
            

def setup(bot):
    bot.add_cog(copyCat(bot))
