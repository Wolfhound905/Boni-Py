# This cog creates voice channels for users
# this may be executed with /room channel_name:name member_cap:optional

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from configuration import get_guilds
from database.voiceVCs import get_voice_channels, add_vc, remove_vc

guilds = get_guilds()


class CreateVC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    options = [
        {
            "name": "channel_name",
            "description": "Name of the voice channel you want to make.",
            "type": 3,
            "required": True
        },
        {
            "name": "member_cap",
            "description": "Optional variable for the number of people allowed in the call.",
            "type": 4,
            "required": False
        }
    ]

    def get_category_by_name(self, guild, category_name):
        category = None
        for c in guild.categories:
            if c.name == category_name:
                category = c
                break
        return category

    @cog_ext.cog_slash(name="room", options=options, description="Create a temperary vc to chat and slam in!", guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, channel_name: str, member_cap=0):
        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.send(hidden=True, content="You need to be in Mouth Chat to use this command.")
        else:
            guild = ctx.guild
            category = self.get_category_by_name(guild, "Voice Channels")
            if member_cap >= 100 or member_cap <= -1:
                await ctx.send(hidden=True, content=f"`{member_cap}` is out of range.\n1-99 is the vailid range for voice channel member caps.")
                return
            channel_name = (channel_name[:97] + '...') if len(channel_name) > 97 else channel_name
            channel = await guild.create_voice_channel(channel_name, user_limit=member_cap, category=category)
            response = await ctx.send(f"I created the voice channel {channel.mention}!")
            add_vc(channel.id, response.channel.id, response.id)
            await ctx.author.move_to(channel=channel)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if len(get_voice_channels()) > 0:
            if before.channel is not None:
                if before.channel.id in get_voice_channels():
                    if len(before.channel.members) == 0:
                        await before.channel.delete()
                        delete_vc = str(before.channel.id)
                        message = remove_vc(delete_vc)
                        message_id: int = message['id']
                        channel_id: int = message['channel']
                        channel = self.bot.get_channel(channel_id)
                        message = channel.get_partial_message(message_id)
                        await message.edit(content=f"Everybody left `{before.channel.name}` so I deleted it.")


def setup(bot):
    bot.add_cog(CreateVC(bot))
