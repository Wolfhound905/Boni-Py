import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from configuration import get_guilds, get_token
import aiohttp
import asyncio
import json

guilds = get_guilds()


class voiceActivities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    options = [
        {          
            "name": "activity_type",
            "description": "Type of activity.",
            "required": True,
            "type": 3,
            "choices": [
                {
                    "name": "YouTube Together",
                    "value": "755600276941176913"
                },
                {
                    "name": "Betrayal.io",
                    "value": "773336526917861400"
                },
                {
                    "name": "Poker Night",
                    "value": "755827207812677713"
                },
                {
                    "name": "Fishington.io",
                    "value": "814288819477020702"
                }
            ]
        }
    ]

    async def get_activity(self, url, api_json, headers):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=api_json, headers=headers) as response:
                print(await response.text())
                data = json.loads(await response.text())
                code = data["code"]
                return code

    @cog_ext.cog_slash(name="activities", options=options, description='Create a voice channel activity', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext,activity_type):
        if ctx.author.voice:
            url = f"https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites"
            api_json = {
                "max_age": 86400,
                "max_uses": 0,
                "target_application_id": f"{activity_type}",
                "target_type": 2,
                "temporary": False,
                "validate": None
                }
            headers = {
                "Authorization": f"Bot {get_token()}",
                "Content-Type": "application/json"
                }

            code = await self.get_activity(url, api_json, headers)
            await ctx.send(f"https://discord.gg/{code} Click on the link to join.")   
        else:
            await ctx.send(hidden=True, content="You need to be in a voice channel.")
        
def setup(bot):
    bot.add_cog(voiceActivities(bot))
