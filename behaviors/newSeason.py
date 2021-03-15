import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from configuration import get_guilds, get_admins

guilds = get_guilds()
admins = get_admins()

class newSeason(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @cog_ext.cog_slash(name="new_season", description='This is for moderator only. EX: /new_season season:17', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, season: int):
        if ctx.author.id in admins:
            increment_new_season(season)
            await ctx.send(f"Season {season} was added to the database.")
            await ctx.send(hidden=True, content="If this was a mistake please contact <@!324352543612469258>")
        else:
            await ctx.respond(eat=True)
            await ctx.send(hidden=True, content="Sorry, you may not use this command.")

def setup(bot):
    bot.add_cog(newSeason(bot))
