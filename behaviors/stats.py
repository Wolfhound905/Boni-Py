import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from database.statsdb import get_guild_stats, get_user_stats
from configuration import get_guilds

#image color stuff
from io import BytesIO
import requests
from PIL import Image


guilds = get_guilds()


class clubMatches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    options = [
        {
            "name": "player",
            "description": "Pick a player to get their stats.",
            "type": 6,
            "required": False,
        },
        {
            "name": "season",
            "description": "Input number of specific season.",
            "type": 4,
            "required": False,
        }
    ]

    @cog_ext.cog_slash(name="stats", options=options, description='Just say /stats to view our current stats!', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, player: discord.Member = None, season: int = None):

        if player is not None:
            stats = get_user_stats(player.id, season)
            if stats is not None:
                s_or_nah = "s"
                if stats['current_streak'][0] == 1:
                    if stats['current_streak'][1] == 1: s_or_nah = ""
                    streak_message = f"They have a current win streak of {stats['current_streak'][1]} game{s_or_nah}." 
                else: 
                    if stats['current_streak'][1] == 1: s_or_nah = ""
                    streak_message = f"They have a current loss streak of {stats['current_streak'][1]} game{s_or_nah}." 

                print(player.avatar_url)
                self.average_hexCode(player.avatar_url)

                embed=discord.Embed(title="⚽ Stats 🚗", color=0xf6c518)
                embed.set_author(name=f"{player.name}'s Season {stats['season']}")
                embed.set_thumbnail(url=player.avatar_url)
                embed.add_field(name="Total Wins", value=f"{player.mention} has won {stats['wins']} matches this season", inline=False)
                embed.add_field(name="Total Losses", value=f"They have lost {stats['losses']} matches :(", inline=False)
                embed.add_field(name="Match Streak", value=streak_message, inline=False)
                embed.add_field(name="Max Streaks", value=f"Their best win streak is {stats['win_streak']} and biggest loss streak is {stats['loss_streak']}.", inline=False)
                embed.set_footer(text="Wording not final :)")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{player.mention} does not have any data recorded for this season yet.", allowed_mentions=discord.AllowedMentions.none())

        else:
            stats = get_guild_stats(season)
            if stats is not None:
                s_or_nah = "s"
                if stats['current_streak'][0] == 1:
                    if stats['current_streak'][1] == 1: s_or_nah = ""
                    streak_message = f"We have a current win streak of {stats['current_streak'][1]} game{s_or_nah}." 
                else: 
                    if stats['current_streak'][1] == 1: s_or_nah = ""
                    streak_message = f"We have a current loss streak of {stats['current_streak'][1]} game{s_or_nah}." 
                
                embed=discord.Embed(title="⚽ Stats 🚗", color=0xf6c518)
                embed.set_author(name=f"Slambonis Season {stats['season']}")
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/610818618325729281/a39b2a8d628ff0a1a20caf44c8e802e5.png")
                embed.add_field(name="Total Wins", value=f"So far we have won {stats['wins']} matches this season", inline=False)
                embed.add_field(name="Total Losses", value=f"We have lost {stats['losses']} matches :(", inline=False)
                embed.add_field(name="Match Streak", value=streak_message, inline=False)
                embed.add_field(name="Max Streaks", value=f"Our best win streak is {stats['win_streak']} and our biggest loss streak is {stats['loss_streak']}.", inline=False)
                embed.set_footer(text="Wording not final :)")
                await ctx.send(embed=embed)
            else:
                await ctx.send("There is no data recorded for this season yet.")



    def average_hexCode(avatar):
        resp = requests.get(avatar)
        assert resp.ok
        img = Image.open(BytesIO(resp.content))
        img2 = img.resize((1, 1))
        color = img2.getpixel((0, 0))
        print('#{:02x}{:02x}{:02x}'.format(*color))

        return(color)
            

def setup(bot):
    bot.add_cog(clubMatches(bot))
