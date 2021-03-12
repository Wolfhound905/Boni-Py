import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class helpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="help", description='Use this command and I will give you the answers to life.', guild_ids = [443884809484238848])
    async def group_say(self, ctx: SlashContext):
        await ctx.send("simple test")
            

def setup(bot):
    bot.add_cog(helpMenu(bot))
