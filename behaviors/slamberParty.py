import discord
from discord.ext import commands
from discord import utils
import asyncio
from database.voiceVCs import (get_voice_channels, add_vc, remove_vc)

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

    async def start_countdown(self):
        await asyncio.sleep(300)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel:
            if after.channel.name == "Slamber Party":
                if len(after.channel.members) <= 3:
                    await self.start_countdown()
                    if len(after.channel.members) <= 3 and after.channel:
                        mouth_chat = discord.utils.get(after.channel.guild.channels, name="Mouth Chat") 
                        for member in after.channel.members:
                            await member.move_to(mouth_chat)
                        await after.channel.delete()
                        remove_vc(after.channel.id)

            else:
                if after.channel and len(after.channel.members) == 4 and after.channel.name == "Mouth Chat":
                    category = self.get_category_by_name(after.channel.guild, "Voice Channels")
                    await after.channel.guild.create_voice_channel(name="Mouth Chat", category=category, position=0)
                    await asyncio.sleep(1)
                    await after.channel.edit(name="Slamber Party", position=1)
                    add_vc(1, after.channel.id, 0, 0)
                    
        elif before.channel:
            if before.channel.name == "Slamber Party":
                if len(before.channel.members) <= 3:
                    await self.start_countdown()
                    if len(before.channel.members) <= 3 and before.channel:
                        mouth_chat = discord.utils.get(before.channel.guild.channels, name="Mouth Chat")
                        for member in before.channel.members:
                            await member.move_to(mouth_chat)
                        await before.channel.delete()
                        remove_vc(before.channel.id)


def setup(bot):
    bot.add_cog(slamberParty(bot))
