import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import os
from dotenv import load_dotenv

load_dotenv()
guilds = []
guilds.append(int(os.getenv('GUILD_ID')))


class newSeason(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @cog_ext.cog_slash(name="new_season", description='This is for moderator only. EX: /new_season season:17', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, season: int):
        if ctx.author.id == 324352543612469258 or ctx.author.id == 329855467591434250 or ctx.author.id == 223406572250988545:
            increment_new_season(season)
            await ctx.send(f"Season {season} was added to the database.")
            await ctx.send(hidden=True, content="If this was a mistake please contact <@!324352543612469258>")
        else:
            await ctx.respond(eat=True)
            await ctx.send(hidden=True, content="Sorry, you may not use this command.")

def setup(bot):
    bot.add_cog(newSeason(bot))
