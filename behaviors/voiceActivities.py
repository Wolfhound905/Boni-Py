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
            "required": False,
            "type": 3,
            "choices": [
                { "name": "YouTube Together", "value": "755600276941176913"},
                { "name": "Betrayal.io", "value": "773336526917861400"},
                { "name": "Poker Night", "value": "755827207812677713"},
                { "name": "Fishington.io", "value": "814288819477020702"}
            ]
        },
        {
            "name": "custom_id",
            "description": "Don't use this unless you know what you are doing 🙃",
            "required": False,
            "type": 3
        }
    ]
    async def get_activity(self, url, api_json, headers):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=api_json, headers=headers) as response:
                data = json.loads(await response.text())
                try:
                    code = data["code"]
                    name = data["target_application"]["name"]
                    logo = f"https://cdn.discordapp.com/app-icons/{data['target_application']['id']}/{data['target_application']['icon']}"
                    activity = {
                        "code": code,
                        "name": name,
                        "logo": logo
                    }
                except KeyError:
                    activity = {
                        "error": f"{data}"
                    }
    
                return activity

    @cog_ext.cog_slash(name="activities", options=options, description='Create a voice channel activity', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, activity_type = None, custom_id = None):
        if activity_type is None and custom_id is None:
            await ctx.send(hidden=True, content="Pick an activity.")
        else:
            if ctx.author.voice:
                url = f"https://discord.com/api/v9/channels/{ctx.author.voice.channel.id}/invites"
                api_json = {
                    "max_age": 86400,
                    "max_uses": 0,
                    "uses": 1,
                    "target_application_id": f"{activity_type if custom_id is None else custom_id}",
                    "target_type": 2,
                    "temporary": False,
                    "validate": None
                    }
                headers = {
                    "Authorization": f"Bot {get_token()}",
                    "Content-Type": "application/json"
                    }


                activity = await self.get_activity(url, api_json, headers)
                try:
                    x = activity["error"]
                    await ctx.send(f"`{x}` Probably means application you are trying to play doesn't exist.🙃")
                except KeyError:                        
                    embed=discord.Embed(color=0x7289DA, title=f"Join {ctx.author.name} in {activity['name']}", description=f"[Click this link](https://discord.gg/{activity['code']}) to start or join {activity['name']} in {ctx.author.voice.channel.name}" )
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.set_thumbnail(url=activity['logo'])
                    await ctx.send(embed=embed)

            else:
                await ctx.send(hidden=True, content="You need to be in a voice channel.")

        
def setup(bot):
    bot.add_cog(voiceActivities(bot))
