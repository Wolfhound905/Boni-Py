import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class getGuilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.Cogs.listener()
async def on_ready():
    get_guilds()

global guilds
guilds = []

def get_guilds():
  for guild in bot.guilds:
    global guilds
    guilds.append(guild.id)
  print(guilds)

def setup(bot):
    bot.add_cog(getGuilds(bot))
