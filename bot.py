# bot.py
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from configuration import get_token, get_guilds


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="./", intents=intents)
slash = SlashCommand(bot, sync_commands=True, override_type = True)
activity = discord.Activity(name='on the ice rink', type=discord.ActivityType.playing)


bot.load_extension("behaviors.clubMatches")
bot.load_extension("behaviors.createVC")
bot.load_extension("behaviors.help")
bot.load_extension("behaviors.copyCat")
bot.load_extension("behaviors.adminCommands")
bot.load_extension("behaviors.welcome")
bot.load_extension("behaviors.exp")



@bot.event
async def on_ready():
    print("ready")
    commands = slash.commands
    print(" Commands ".center(14, "~"))
    await bot.change_presence(activity=activity)
    for key in commands:
        print(commands[key].name)
    print("⸻⸻⸻⸻") 


  
bot.run(get_token())
