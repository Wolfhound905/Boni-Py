# bot.py
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
guilds = int(os.getenv('GUILD_ID'))

bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot, sync_commands=True, override_type = True)
activity = discord.Activity(name='with some code', type=discord.ActivityType.playing)


bot.load_extension("behaviors.clubMatches")
bot.load_extension("behaviors.createVC")
bot.load_extension("behaviors.help")
bot.load_extension("behaviors.copyCat")
bot.load_extension("behaviors.newSeason")


@bot.event
async def on_ready():
    print("ready")
    commands = slash.commands
    print(" Commands ".center(14, "~"))
    await bot.change_presence(activity=activity)
    for key in commands:
        print(commands[key].name)
    print("⸻⸻⸻⸻") 
  

  
bot.run(TOKEN)
