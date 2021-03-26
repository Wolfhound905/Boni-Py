# This cog is for admins only and just repeats what you give it


import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from configuration import get_guilds, get_admins

guilds = get_guilds()
admins = get_admins()

class copyCat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="say", description='Enter a message and I will repeat it :)', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, message: str):
        if ctx.author.id in admins:
            await ctx.respond(eat=True)
            await ctx.send(hidden=True, content="Message sent successfully")
            await ctx.send(message)
        else:
            await ctx.respond(eat=True)
            await ctx.send(hidden=True, content="No ♥")


def setup(bot):
    bot.add_cog(copyCat(bot))
