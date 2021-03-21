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
        Messages = {
            "W1": ["Way to rep the club!",
                   "Wow! You guys are on a roll!",
                   "Now that’s how you slam!",
                   "I wanna grow up to slam as hard as you guys one day!",
                   "They won’t forget the day they lost to the Slambonis!",
                   "You guys really left em skidding on the rink!", ],
            "W2": ["Do you think we should go pro?", 
                   "RLCS here we come!",
                   "Maybe we should let them win for a change?",
                   "Does this mean we get jerseys and would they make them in my size… and shape?"],
            "W3": ["Guess what, I just signed us up for RLCS. I wasn’t joking earlier.",
                   "If you guys keep this up I’ll have to get us a sponsor!",
                   "Ok so I’m not pointing any wheels here but... You guys are reporting losing right?"],
            "L1": ["Aw man…",
                   "I still think we’re the best club around!",
                   "At least we had fun",
                   'Papa Boni always used to say "Sometimes you slam, sometimes you get slammed"',
                   "Darn. I forgot what I was gonna to say…",
                   "Well we’ve still got each other"],
            "L2": ["Momma Boni said there'd be days like this.",
                   "This would crush a weaker club. But not us!",
                   "It’s not looking good. But. We’ve seen worse… Right?"],
            "L3": ["This hurts. Does this hurt for you guys? This hurts me physically.",
                   "Don’t worry guys. I have a feeling they’re getting tired of beating us!",
                   "Hey guys. Can we take a water break? I need a minute."]}

        if match == "win":
            increment_win()
            stats = get_stats()
            if stats.win_streak <= 3: win_messages = Messages["W1"]
            elif stats.win_streak <= 6: win_messages = Messages["W2"]
            else: win_messages = Messages["W3"]
            await ctx.send(f"{random.choice(win_messages)} \nCurrent win streak is: {str(stats.win_streak)}")

        elif match == "loss":
            increment_loss()
            stats = get_stats()
            if stats.loss_streak <= 3: loss_messages = Messages["L1"]
            elif stats.loss_streak <= 6: loss_messages = Messages["L2"]
            else: loss_messages = Messages["L3"]
            await ctx.send(f"{random.choice(loss_messages)} \nCurrent loss streak is: {str(stats.loss_streak)}")
            
        elif match == "stats":
            stats = get_stats()
            s_or_nah = "s"
            if stats.win_streak > stats.loss_streak:
                if stats.win_streak == 1: s_or_nah = ""
                streak_message = f"We have a current win streak of {stats.win_streak} game{s_or_nah}." 
            else: 
                if stats.loss_streak == 1: s_or_nah = ""
                streak_message = f"We have a current loss streak of {stats.loss_streak} game{s_or_nah}." 
            
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
