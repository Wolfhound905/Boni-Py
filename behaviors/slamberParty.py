import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from configuration import get_guilds
from database.voiceVCs import get_voice_channels, add_vc, remove_vc

guilds = get_guilds()


class slamberParty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_category_by_name(self, guild, category_name):
        category = None
        for c in guild.categories:
            if c.name == category_name:
                category = c
                break
        return category

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel.guild.id != 610818618325729281: # This is so we don't spoil the feature!
            if after.channel and len(after.channel.members) == 4 and after.channel.name == "Mouth Chat":
                guild = after.channel.guild
                category = self.get_category_by_name(guild, "Voice Channels")
                channel = await guild.create_voice_channel("Slamber Party", category=category)
                channel_id = str(channel.id)
                add_vc(channel_id)
                for members in after.channel.members:
                    await members.move_to(channel=channel)
        



def setup(bot):
    bot.add_cog(slamberParty(bot))
