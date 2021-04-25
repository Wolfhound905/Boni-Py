import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from configuration import get_guilds, get_admins
import os
import asyncio
import re

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

    @commands.command(
        name="status", description="./status <playing, listening> <input>    remember that listening already has `to` by default"
    )
    @commands.is_owner()
    async def status(self, ctx, arg, *, args):
        if arg == "playing":
            activity = discord.ActivityType.playing
        elif arg == "listening":
            activity = discord.ActivityType.listening
        elif arg == "watching":
            activity = discord.ActivityType.watching

        activity = discord.Activity(name=args, type=activity)
        await self.bot.change_presence(activity=activity)

    @commands.command(
        name="members", description="get members"
    )
    @commands.is_owner()
    async def members(self, ctx):
        guild_members = ctx.guild.members
        for Member in guild_members:
            if not Member.bot: await ctx.send(Member.avatar_url)
        
        


def setup(bot):
    bot.add_cog(adminCommands(bot))
