import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(ctx, member)
    ctx.send(f"""
    Woah! Who’s this? @everyone say hello and welcome {member}! It's good to meet you. 
    I'm Boni, and my friends here are The Slambonis! I'm sure you're excited to get slammin', 
    so I'll skate on out of here so you can get started!!! Just remember our motto “Always slam with fam but never slam fam”!
    """)


def setup(bot):
    bot.add_cog(welcome(bot))
