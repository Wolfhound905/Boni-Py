import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dotenv import load_dotenv
import psycopg2
import random
import os

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
            con = psycopg2.connect(db)
            cur = con.cursor()
            # Example: "wins" is row[0]
            cur.execute(
                "SELECT wins, losses, win_streak, loss_streak from stats")
            rows = cur.fetchall()
            for row in rows:
                wins = row[0]
                losses = row[1]
                win_streak = row[2]
                loss_streak = row[3]
            cur.execute(
                f"UPDATE stats SET wins = {str(wins + 1)}, win_streak = {str(win_streak + 1)}, loss_streak= 0 WHERE wins={str(wins)} AND losses={str(losses)} AND win_streak={str(win_streak)} AND loss_streak={str(loss_streak)}")
            con.commit()
            con.close()
            await ctx.send(f"{random.choice(win_messages)} \nCurrent win streak is: {str(win_streak + 1)}")

        elif result == "loss":
            con = psycopg2.connect(db)
            cur = con.cursor()
            # Example: "wins" is row[0]
            cur.execute(
                "SELECT wins, losses, win_streak, loss_streak from stats")
            rows = cur.fetchall()
            for row in rows:
                wins = row[0]
                losses = row[1]
                win_streak = row[2]
                loss_streak = row[3]
            cur.execute(
                f"UPDATE stats SET losses = {str(losses + 1)}, loss_streak = {str(loss_streak + 1)}, win_streak= 0 WHERE wins={str(wins)} AND losses={str(losses)} AND win_streak={str(win_streak)} AND loss_streak={str(loss_streak)}")
            con.commit()
            con.close()
            await ctx.send(f"{random.choice(loss_messages)} \nCurrent loss streak is: {str(loss_streak + 1)}")
        elif result == "stats":
            con = psycopg2.connect(db)
            cur = con.cursor()
            # Example: "wins" is row[0]
            cur.execute(
                "SELECT wins, losses, win_streak, loss_streak from stats")
            rows = cur.fetchall()
            for row in rows:
                wins = row[0]
                losses = row[1]
                win_streak = row[2]
                loss_streak = row[3]

        else:
            await ctx.respond(await ctx.send_hidden("Incorrect format please use. `/match <win/loss>`"))


def setup(bot):
    bot.add_cog(clubMatches(bot))
