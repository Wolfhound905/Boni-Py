import discord
from discord.ext import commands
from configuration import get_welcome_channel

channelID = int(get_welcome_channel())

class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 610818618325729281:
            await self.bot.get_channel(channelID).send(
            f"Woah! Who’s this? @everyone say hello and welcome {member.mention}! It's good to meet you."
            " I'm Boni, and my friends here are The Slambonis! I'm sure you're excited to get slammin'"
            " so I'll skate on out of here so you can get started!!! Just remember our motto, “Always slam with fam but never slam fam”! <:Boni:696826675153076325>"
            )

def setup(bot):
    bot.add_cog(welcome(bot))
