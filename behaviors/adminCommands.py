import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from configuration import get_guilds, get_admins

guilds = get_guilds()
admins = get_admins()

class adminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    # @commands.command(name="New Season")
    # async def new_season(self, ctx):
    #     """ Creates a new season "./new_season" """
    #     if ctx.author.id in admins:
    #         increment_new_season()
    #         stats = get_stats()
    #         season = str(stats.season)
    #         await ctx.send(f"Season {season} was added to the database.")
    #     else:
    #         await ctx.send("Sorry, you may not use this command.")

def setup(bot):
    bot.add_cog(adminCommands(bot))
