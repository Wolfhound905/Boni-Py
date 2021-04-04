import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from database.user_xp import add_xp, get_xp
from configuration import get_guilds, get_admins


guilds = get_guilds()
admins = get_admins()


class xp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    options = [
        {
            "name": "person",
            "description": "The user you want to give xp to",
            "type": 6,
            "required":True,
        },
        {
            "name": "give",
            "description": "Amount of xp to give user.",
            "type": 4,
            "required":False,
        }
    ]

    @cog_ext.cog_slash(name="xp", options=options, description='Provide xp to active participents', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, name: discord.Member, give = 0):
        user_id = name.id 
        if give == 0:
            # add_xp(user_id, give)
            await ctx.send(f"{name.mention} has a total of {get_xp(user_id)} slam points.", allowed_mentions=discord.AllowedMentions.none())
        elif ctx.author.id in admins:
            await add_xp(user_id, give, self.bot)
            await ctx.send(f"Added {give} slam points to {name.mention}. Bringing them to a total of {get_xp(user_id)} slam points.", allowed_mentions=discord.AllowedMentions.none())
        else:
            await ctx.send(hidden=True, content="You do not have permission to edit points. Here are the user's stats")
            await ctx.send(f"{name.mention} has a total of {get_xp(user_id)} slam points.", allowed_mentions=discord.AllowedMentions.none())


def setup(bot):
    bot.add_cog(xp(bot))
