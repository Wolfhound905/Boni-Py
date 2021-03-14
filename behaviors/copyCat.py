import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import os
from dotenv import load_dotenv

load_dotenv()
guilds = []
guilds.append(int(os.getenv('GUILD_ID')))


class copyCat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="say", description='Enter a message and I will repeat it :)', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, message: str):
        if ctx.author.id == 324352543612469258 or ctx.author.id == 329855467591434250:
            await ctx.respond(await ctx.send_hidden("Message sent successfully"))
            await ctx.send(message)
        else:
            await ctx.respond(await ctx.send_hidden("No ♥"))


def setup(bot):
    bot.add_cog(copyCat(bot))
