import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from configuration import get_guilds

guilds = get_guilds()

class helpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    @cog_ext.cog_slash(name="help", description='Use this command and I will give you the answers to life.', guild_ids = guilds)
    async def group_say(self, ctx: SlashContext):
        embed=discord.Embed(title="Help Menu", description="A list of all slash commands to use with Boni", color=0xf6c518)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="/club", value="This command allows you to report matches after you have a club match in Rocket League\n    Example: `/club match:<win|loss> player_2:@Boni overtime:<True|False>`", inline=False)
        embed.add_field(name="/room", value="This command creates a custom voice channel that you can chat in.\n    Example: `/room channel_name:Test member_cap:10 `", inline=False)
        embed.add_field(name="/stats", value="Example Server Stats: `/stats` \n    Example Player Stats: `/stats player:@Boni`", inline=False)
        embed.add_field(name="/xp", value="View a members Slam Points™\n    Example: `/xp person:@Boni`", inline=False)
        embed.set_footer(text="Keep on slamin'", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)        
def setup(bot):
    bot.add_cog(helpMenu(bot))
