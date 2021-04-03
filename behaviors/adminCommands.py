import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from configuration import get_guilds, get_admins

guilds = get_guilds()
admins = get_admins()

class adminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
                name='reload', description="Reload all/one of the bots cogs!"
            )
    @commands.is_owner()
    async def _reload(self, ctx, cog=None):
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs.",
                    color=0xf6c518,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./behaviors/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"behaviors.{ext[:-3]}")
                            self.bot.load_extension(f"behaviors.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./behaviors/{ext}"):
                    # if the file does not exist
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"behaviors.{ext[:-3]}")
                        self.bot.load_extension(f"behaviors.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)

    # @commands.command(name="New Season")
    # async def new_season(self, ctx):
    #     """ Creates a new season "./new_season" """
    #     if ctx.author.id in admins:
    #         increment_new_season()
    #         stats = get_stats()
    #         season = str(stats.season)
    #         await ctx.send(f"Season {season} was added to the database.")
    #     else:
    #         await ctx.send("Sorry, you may not use this command.")

def setup(bot):
    bot.add_cog(adminCommands(bot))
