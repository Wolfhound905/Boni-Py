import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from database.statsdb import get_guild_stats, get_user_stats
from configuration import get_guilds
import datetime

#image color stuff
from io import BytesIO
import requests
from PIL import Image


guilds = get_guilds()



class clubMatches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def pfp_embedColor(self, player):
        resp = requests.get(player.avatar_url)
        assert resp.ok
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        img2 = img.resize((1, 1))
        color = img2.getpixel((0, 0))
        color = discord.Color.from_rgb(color[0], color[1], color[2])
        return(color)


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

                wins: int = stats['wins']
                losses: int = stats['losses']
                current_streak: int = stats['current_streak']

                embed_color = self.pfp_embedColor(player)
                embed = discord.Embed(title="User Stats", color=embed_color, description="You can view other's stats with `/stats player: @person` \n ⸻⸻⸻⸻⸻⸻⸻⸻", timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=player.avatar_url)
                embed.set_author(name=f"{player.name}'s Season {stats['season']}", icon_url=player.avatar_url)
                embed.add_field(name="Wins", value=stats['wins'], inline=True)
                embed.add_field(name="Losses", value=stats['losses'], inline=True)
                embed.add_field(name="Win Percentage", value=f"{round(((wins / (wins + losses)) * 100), 2)}%", inline=True)
                embed.add_field(name="Current Streak", value=f"{current_streak[1]}{(' wins' if current_streak[1] >= 2 else ' win') if current_streak[0] == 1 else (' losses' if current_streak[1] >= 2 else ' loss')}", inline=True)
                embed.add_field(name="Best Win Streak", value=stats['win_streak'], inline=True)
                embed.add_field(name="Worst Loss Streak", value=stats['loss_streak'], inline=True)
                embed.set_footer(text="Keep on slamin'", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"{player.mention} does not have any data recorded for this season yet.", allowed_mentions=discord.AllowedMentions.none())

        else:
            stats = get_guild_stats(season)
            if stats is not None:
                
                wins: int = stats['wins']
                losses: int = stats['losses']
                current_streak: int = stats['current_streak']

                embed = discord.Embed(title="Server Stats", color=0xf6c518, description="View our stats any time with `/stats` \n ⸻⸻⸻⸻⸻⸻⸻⸻", timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.set_author(name=f"Slambonis Season {stats['season']}", icon_url=ctx.guild.icon_url)
                embed.add_field(name="Wins", value=stats['wins'], inline=True)
                embed.add_field(name="Losses", value=stats['losses'], inline=True)
                embed.add_field(name="Win Percentage", value=f"{round(((wins / (wins + losses)) * 100), 2)}%", inline=True)
                embed.add_field(name="Current Streak", value=f"{current_streak[1]}{(' wins' if current_streak[1] >= 2 else ' win') if current_streak[0] == 1 else (' losses' if current_streak[1] >= 2 else ' loss')}", inline=True)
                embed.add_field(name="Best Win Streak", value=stats['win_streak'], inline=True)
                embed.add_field(name="Worst Loss Streak", value=stats['loss_streak'], inline=True)
                embed.set_footer(text="Keep on slamin'", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)


            else:
                await ctx.send("There is no data recorded for this season yet.")
            
def setup(bot):
    bot.add_cog(clubMatches(bot))

