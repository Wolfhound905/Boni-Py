import discord
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from configuration import get_guilds, get_admins
from database.user_xp import check_for_reward_removal

guilds = get_guilds()
admins = get_admins()

class rewardRemover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_for_removal.start()

    
    @tasks.loop(hours=6.0)
    async def check_for_removal(self):
        await check_for_reward_removal(self.bot)

    def cog_unload(self):
        self.check_for_removal.cancel()

def setup(bot):
    bot.add_cog(rewardRemover(bot))
