import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class CreateVC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="vc", name="create", description="Create a temperary vc to chat and slam in!", guild_ids = [443884809484238848])
    async def group_say(self, ctx: SlashContext, channel: str):
        guild = ctx.guild
        channel = await guild.create_voice_channel(channel)
        await ctx.send("Created the vc `" + str(channel) + "`!")


def setup(bot):
    bot.add_cog(CreateVC(bot))
