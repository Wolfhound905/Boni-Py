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
                { "name": "YouTube Together", "value": "1"}, { "name": "Betrayal.io", "value": "2" },
                { "name": "Poker Night", "value": "3"}, { "name": "Fishington.io", "value": "4" }
            ]
        }
    ]

    activities = {
        "1": { "name": "YouTube Together", "id": "755600276941176913", "logo": "https://cdn.discordapp.com/attachments/780435741650059268/836350004204798010/yt-icon.png"},
        "2": { "name": "Betrayal", "id": "773336526917861400", "logo": "https://betrayal.io/asset/image/share-card-betrayal.png"},
        "3": { "name": "Poker Night", "id": "755827207812677713", "logo": "https://media.discordapp.net/attachments/780435741650059268/836354650013171772/unknown.png?width=822&height=676"},
        "4": { "name": "Fishington", "id": "814288819477020702", "logo": "https://betrayal.io/asset/image/share-card-fishington.png"}
    }

    async def get_activity(self, url, api_json, headers):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=api_json, headers=headers) as response:
                data = json.loads(await response.text())
                code = data["code"]
                return code

    @cog_ext.cog_slash(name="activities", options=options, description='Create a voice channel activity', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, activity_type):
        if ctx.author.voice:
            url = f"https://discord.com/api/v9/channels/{ctx.author.voice.channel.id}/invites"
            api_json = {
                "max_age": 86400,
                "max_uses": 0,
                "target_application_id": f"{self.activities[activity_type]['id']}",
                "target_type": 2,
                "temporary": False,
                "validate": None
                }
            headers = {
                "Authorization": f"Bot {get_token()}",
                "Content-Type": "application/json"
                }

            code = await self.get_activity(url, api_json, headers)


            embed=discord.Embed(title=f"Join {ctx.author.name} in {self.activities[activity_type]['name']}", description=f"[Click this link](https://discord.gg/{code}) to start or join {self.activities[activity_type]['name']} in {ctx.author.voice.channel.name}")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=self.activities[activity_type]['logo'])
            await ctx.send(embed=embed)
        else:
            await ctx.send(hidden=True, content="You need to be in a voice channel.")
        
def setup(bot):
    bot.add_cog(voiceActivities(bot))
