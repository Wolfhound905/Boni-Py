import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @cog_ext.cog_slash(name="embed", guild_ids = [443884809484238848])
    # async def _test(self, ctx: SlashContext):
    #     embed = discord.Embed(title="embed test")
    #     await ctx.send(content="te", embeds=[embed])

def setup(bot):
    bot.add_cog(Slash(bot))
