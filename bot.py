# bot.py
import os
from dotenv import load_dotenv

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot, sync_commands=True, override_type = True)

bot.load_extension("behaviors.clubMatches")
bot.load_extension("behaviors.createVC")
bot.load_extension("behaviors.help")


@bot.event
async def on_ready():
    print("ready")
    commands = slash.commands
    print("commands".center(20, "#"))
    for key in commands:
        print(commands[key].name)
    #await slash.sync_all_commands()


bot.run(TOKEN)
