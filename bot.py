# bot.py
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from configuration import get_token, get_guilds

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="./", intents=intents)
slash = SlashCommand(bot, sync_commands=True)
activity = discord.Activity(name='on the ice rink', type=discord.ActivityType.playing)


bot.load_extension("behaviors.clubMatches")
bot.load_extension("behaviors.room")
bot.load_extension("behaviors.help")
bot.load_extension("behaviors.copyCat")
bot.load_extension("behaviors.adminCommands")
bot.load_extension("behaviors.welcome")
bot.load_extension("behaviors.xp")
bot.load_extension("behaviors.slamberParty")
bot.load_extension("behaviors.stats")
bot.load_extension("behaviors.voiceActivities")

@bot.event
async def on_ready():
    bot.load_extension("behaviors.rewardRemover")
    print("ready")
    commands = slash.commands
    await bot.change_presence(activity=activity)
    print(" Commands ".center(14, "~"))
    for key in commands:
        print(commands[key].name)
    print("⸻⸻⸻⸻")     


  
bot.run(get_token())
