import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dotenv import load_dotenv
import psycopg2
import random
import os
from database.statsdb import increment_loss, increment_win, get_stats, Stats

load_dotenv()
guilds = []
guilds.append(int(os.getenv('GUILD_ID')))
db = os.getenv('DB')


class clubMatches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="match", description='Let me know if we had a "win" or a "loss". Or you can check our stats with "stats"', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, result: str):
        win_messages = [
            "Way to rep the club!", "Wow! You guys are on a roll!", "Now that’s how you slam!",
            "I wanna grow up to slam as hard as you guys one day!", "They won’t forget the day they lost to the Slambonis!",
            "Do you think we should go pro?", "RLCS here we come!"
        ]
        loss_messages = [
            "Aw man…", "I still think we’re the best club around!", "At least we had fun",
            "Papa Boni always used to say “Sometimes you slam, sometimes you get slammed”",
            "Darn. I forgot what I was gonna to say…", "Well we’ve still got each other"
        ]

        if result == "win":
            increment_win()
            stats = get_stats()
            
            await ctx.send(f"{random.choice(win_messages)} \nCurrent win streak is: {str(stats.win_streak)}")

        elif result == "loss":
            increment_loss()
            stats = get_stats()
            
            await ctx.send(f"{random.choice(loss_messages)} \nCurrent loss streak is: {str(stats.loss_streak)}")
        elif result == "stats":
            stats = get_stats()
                
        else:
            await ctx.respond(await ctx.send_hidden("Incorrect format please use. `/match <win/loss>`"))


def setup(bot):
    bot.add_cog(clubMatches(bot))
