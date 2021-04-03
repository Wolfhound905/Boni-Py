from dotenv import load_dotenv
import os

# dictionary used to store env's in memory
env = {}


def load_env():
    load_dotenv()

    env["DISCORD_TOKEN"] = os.getenv('DISCORD_TOKEN')

    env["GUILD_ID"] = []
    for guild in os.getenv('GUILD_ID').split(","):
        env["GUILD_ID"].append(int(guild.strip()))

    env["ADMINS"] = []
    for admin in os.getenv('ADMINS').split(","):
        env["ADMINS"].append(int(admin.strip()))

    env["USER_NAME"] = os.getenv("USER_NAME")

    env["PASSWORD"] = os.getenv("PASSWORD")

    env["HOST"] = os.getenv("HOST")

    env["DATABASE"] = os.getenv("DATABASE")

    env["WELCOME_CHANNEL"] = os.getenv("WELCOME_CHANNEL")

    env["REWARD_ROLE_ID"] = os.getenv("REWARD_ROLE_ID")

    env["REWARD_THRESHOLD"] = int(os.getenv("REWARD_THRESHOLD"))


def get_guilds() -> list:
    return env["GUILD_ID"]

def get_welcome_channel() -> int:
    return env["WELCOME_CHANNEL"]


def get_token() -> str:
    return env["DISCORD_TOKEN"]


def get_user_name() -> str:
    return env["USER_NAME"]


def get_password() -> str:
    return env["PASSWORD"]


def get_host() -> str:
    return env["HOST"]


def get_database() -> str:
    return env["DATABASE"]


def get_admins() -> list:
    return env["ADMINS"]

def get_reward_role() -> int:
    return env["REWARD_ROLE_ID"]

def get_reward_threshold() -> int:
    return env["REWARD_THRESHOLD"]


# load enviroment variables on startup
load_env()
