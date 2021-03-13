import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import os 
from dotenv import load_dotenv

load_dotenv()
guilds = []
guilds.append(int(os.getenv('GUILD_ID')))

class helpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    @cog_ext.cog_slash(name="help", description='Use this command and I will give you the answers to life.', guild_ids = guilds)
    async def group_say(self, ctx: SlashContext):
        embed=discord.Embed(title="Help Menu", description="A list of all slash commands to use with Boni", color=0xf6c518)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/819606905735479356/f30474b0aa66b3541bfdacf5bad5783a.png")
        embed.add_field(name="/room", value="Example: `/room channel_name:Test member_cap:10 `", inline=False)
        embed.add_field(name="/match", value="Example: `/match result:win `", inline=False)
        embed.set_footer(text="If you have any questions and suggestions ask Wolf")
        await ctx.send(embed=embed)        

def setup(bot):
    bot.add_cog(helpMenu(bot))
