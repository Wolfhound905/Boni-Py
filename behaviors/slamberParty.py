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


# guild = ctx.guild
# category = self.get_category_by_name(guild, "Voice Channels")
# if member_cap >= 100:
#     await ctx.respond(await ctx.send_hidden("Incorrect member cap on channel!\n1-99 is the vailid range for a member cap."))
#     return
# channel = await guild.create_voice_channel(channel_name, user_limit=member_cap, category=category)
# await ctx.send(f"I created the voice channel `{channel_name}`!")
# channel_id = str(channel.id)
# add_vc(channel_id)
# await ctx.author.move_to(channel=channel)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
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
