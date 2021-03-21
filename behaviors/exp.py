import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
# from database.user_exp import 
from configuration import get_guilds


guilds = get_guilds()


class exp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    options = [
        {
            "name": "give",
            "description": "Amount of xp to give user.",
            "type": 4,
            "required":True,
        },
        {
            "name": "person",
            "description": "The user you want to give xp to",
            "type": 6,
            "required":True,
        }
    ]

    @cog_ext.cog_slash(name="xp", options=options, description='Provide xp to active participents', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, give: int, name: discord.Member):
        member_id = name.id
        print(member_id)    

def setup(bot):
    bot.add_cog(exp(bot))
