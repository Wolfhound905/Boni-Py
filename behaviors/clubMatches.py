import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import random
from database.statsdb import increment_loss, increment_win, increment_new_season, get_stats, Stats
from configuration import get_guilds


guilds = get_guilds()


class clubMatches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    options = [
        {
            "name": "match",
            "description": "Win/loss report club matches.",
            "type": 3,
            "required":False,
            "choices": [
                {
                    "name": "win",
                    "value": "win"
                },
                {
                    "name": "loss",
                    "value": "loss"
                },
                {
                    "name": "stats",
                    "value": "stats"
                }
            ]
        }
    ]

    @cog_ext.cog_slash(name="club", options=options, description='Reports wins and losses or even view our stats!', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, match: str):
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

        if match == "win":
            increment_win()
            stats = get_stats()
            
            await ctx.send(f"{random.choice(win_messages)} \nCurrent win streak is: {str(stats.win_streak)}")

        elif match == "loss":
            increment_loss()
            stats = get_stats()
            
            await ctx.send(f"{random.choice(loss_messages)} \nCurrent loss streak is: {str(stats.loss_streak)}")
            
        elif match == "stats":
            stats = get_stats()
            if stats.win_streak > stats.loss_streak:
                streak_message = f"We have a current win streak of {stats.win_streak} games." 
            else: 
                streak_message = f"We have a current loss streak of {stats.loss_streak} games." 
            embed=discord.Embed(title="⠀", color=0xf6c518)
            embed.set_author(name=f"Slambonis Season {stats.season}")
            embed.set_thumbnail(url="https://cdn.discordapp.com/icons/610818618325729281/a39b2a8d628ff0a1a20caf44c8e802e5.png")
            embed.add_field(name="Total Wins", value=f"So far we have won {stats.wins} matches this season", inline=False)
            embed.add_field(name="Total Losses", value=f"We have lost {stats.losses} matches :(", inline=False)
            embed.add_field(name="Streak", value=streak_message, inline=False)
            embed.add_field(name="Max Streaks", value=f"Our best win streak is {stats.max_win_streak} and our biggest loss streak is {stats.max_loss_streak}.", inline=False)
            embed.set_footer(text="Wording not final :)")
            await ctx.send(embed=embed)
                
        else:
            await ctx.respond(eat=True)
            await ctx.send( hidden=True, content="Incorrect format please use. `/club match:<win/loss/stats>`")


def setup(bot):
    bot.add_cog(clubMatches(bot))
