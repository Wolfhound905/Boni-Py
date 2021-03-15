from dotenv import load_dotenv
import os

#dictionary used to store env's in memory
env = {}

def load_env():
    load_dotenv()

    env["DISCORD_TOKEN"] = os.getenv('DISCORD_TOKEN')

    env["GUILD_ID"] = []
    for guild in os.getenv('GUILD_ID').split(","):
        env["GUILD_ID"].append(int(guild.strip()))

    env["DB"] = os.getenv('DB')

    env["ADMINS"] = []
    for admin in os.getenv('ADMINS').split(","):
        env["ADMINS"].append(int(admin.strip()))


def get_guilds() -> list:
    return env["GUILD_ID"]

def get_token() -> str:
    return env["DISCORD_TOKEN"]

def get_db() -> str:
    return env["DB"]

def get_admins() -> list:
    return env["ADMINS"]

#load enviroment variables on startup
load_env()