# This cog is for the reporting of club wins and losses.
# A user can execute this command with /club match:result

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import random
from database.statsdb import add_match, get_guild_stats, update_users
from configuration import get_guilds
from database.user_xp import add_xp


guilds = get_guilds()


class clubMatches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    win_messages = {
        0:  ["Way to rep the club!",
                "Wow! You guys are on a roll!",
                "Now that’s how you slam!",
                "I wanna grow up to slam as hard as you guys one day!",
                "They won’t forget the day they lost to the Slambonis!",
                "You guys really left em skidding on the rink!", ],
        4:  ["Do you think we should go pro?", 
                "RLCS here we come!",
                "Maybe we should let them win for a change?",
                "Does this mean we get jerseys and would they make them in my size… and shape?"],
        7:  ["Guess what, I just signed us up for RLCS. I wasn’t joking earlier.",
                "If you guys keep this up I’ll have to get us a sponsor!",
                "Ok so I’m not pointing any wheels here but... You guys are reporting losing right?"]}

    loss_messages= {        
        0:  ["Aw man…",
                "I still think we’re the best club around!",
                "At least we had fun",
                'Papa Boni always used to say "Sometimes you slam, sometimes you get slammed"',
                "Darn. I forgot what I was gonna to say…",
                "Well we’ve still got each other"],
        4:  ["Momma Boni said there'd be days like this.",
                "This would crush a weaker club. But not us!",
                "It’s not looking good. But. We’ve seen worse… Right?"],
        7:  ["This hurts. Does this hurt for you guys? This hurts me physically.",
                "Don’t worry guys. I have a feeling they’re getting tired of beating us!",
                "Hey guys. Can we take a water break? I need a minute."]}

    options = [
        {
            "name": "match",
            "description": "Win/loss report club matches.",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "win",
                    "value": "win"
                },
                {
                    "name": "loss",
                    "value": "loss"
                },
            ]
        },
        {
            "name": "player_2",
            "description": "People in club match.",
            "type": 6,
            "required": True,
        },
        {
            "name": "player_3",
            "description": "People in club match.",
            "type": 6,
            "required": False,
        },
        {
            "name": "player_4",
            "description": "People in club match.",
            "type": 6,
            "required": False,
        },
        {
            "name": "overtime",
            "description": "Did your match go into overtime?",
            "type": 5,
            "required": False,
        }

    ]

    @cog_ext.cog_slash(name="club", options=options, description='Reports wins and losses!', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, match: str, player_2: discord.Member, overtime: bool = None, player_3: discord.Member = None, player_4: discord.Member = None):
        player_1: discord.Member = ctx.author

        if match == "win":
            add_match(True, player_1, player_2, player_3, player_4, overtime)
            update_users(ctx.guild.members)
            stats = get_guild_stats()
            message = self._get_message(stats['win_streak'], self.win_messages)
            await ctx.send(f"{message} \nCurrent win streak is: {str(stats['current_streak'][1])}")

        elif match == "loss":
            add_match(False, player_1, player_2, player_3, player_4, overtime)
            update_users(ctx.guild.members)
            stats = get_guild_stats()
            message = self._get_message(stats['loss_streak'], self.loss_messages)
            await ctx.send(f"{message} \nCurrent loss streak is: {str(stats['current_streak'][1])}")
        else:
            await ctx.send(hidden=True, content="Incorrect format please use. `/club match:<win/loss>`")

    def _get_message(self, streak: int, messages: dict):
        for streak_threshold in sorted(messages.keys()):
            if streak >= int(streak_threshold):
                return random.choice(messages[streak_threshold])

def setup(bot):
    bot.add_cog(clubMatches(bot))
