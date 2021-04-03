import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from database.statsdb import get_guild_stats
from configuration import get_guilds


guilds = get_guilds()


class clubMatches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    options = [
        {
            "name": "season",
            "description": "Input number of specific season.",
            "type": 4,
            "required": False,
        }
    ]

    @cog_ext.cog_slash(name="stats", options=options, description='Just say /stats to view our current stats!', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, season: int = None):
        stats = get_guild_stats(season)

        s_or_nah = "s"
        if stats['current_streak'][0] == 1:
            if stats['current_streak'][1] == 1: s_or_nah = ""
            streak_message = f"We have a current win streak of {stats['current_streak'][1]} game{s_or_nah}." 
        else: 
            if stats['current_streak'][1] == 1: s_or_nah = ""
            streak_message = f"We have a current loss streak of {stats['current_streak'][1]} game{s_or_nah}." 
        
        embed=discord.Embed(title="⠀", color=0xf6c518)
        embed.set_author(name=f"Slambonis Season {stats['season']}")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/610818618325729281/a39b2a8d628ff0a1a20caf44c8e802e5.png")
        embed.add_field(name="Total Wins", value=f"So far we have won {stats['wins']} matches this season", inline=False)
        embed.add_field(name="Total Losses", value=f"We have lost {stats['losses']} matches :(", inline=False)
        embed.add_field(name="Streak", value=streak_message, inline=False)
        embed.add_field(name="Max Streaks", value=f"Our best win streak is {stats['win_streak']} and our biggest loss streak is {stats['loss_streak']}.", inline=False)
        embed.set_footer(text="Wording not final :)")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(clubMatches(bot))
