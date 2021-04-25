import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from configuration import get_guilds, get_token
import requests
import json

guilds = get_guilds()


class activities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    options = [
        {
            "name": "channel",
            "description": "Select the voice channel you want.",
            "type": 7,
            "required":True,
        },
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

    @cog_ext.cog_slash(name="activity", options=options, description='Create a voice channel activity', guild_ids=guilds)
    async def group_say(self, ctx: SlashContext, channel, activity_type):
        if ctx.author.voice:
            if channel.type == discord.ChannelType.voice:
                url = f"https://discord.com/api/v8/channels/{channel.id}/invites"
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
                api_return = requests.post(url, json=api_json, headers=headers)
                data = json.loads(api_return.text)
                code = data["code"]
                await ctx.send(f"https://discord.gg/{code} Click on the link to join.")   
            else:
                await ctx.send(hidden=True, content="Please select a voice channel.")
        else:
            await ctx.send(hidden=True, content="You need to be in a voice channel.")
        
def setup(bot):
    bot.add_cog(activities(bot))
