from interactions import (
    Button,
    ComponentContext,
    Extension,
    Client,
    IntervalTrigger,
    SlashCommand,
    Permissions,
    GuildText,
    SlashContext,
    StringSelectMenu,
    StringSelectOption,
    Task,
    slash_command,
    slash_option,
    OptionType,
    ChannelType,
    Embed,
    listen,
    events,
)
from random import choice

warehouse_channel_id = 819980437329543180


class Destiny(Extension):
    def __init__(self, bot: Client):
        self.bot: Client = bot

    @slash_command(name="gambit", description="Who we versing?")
    async def gambit(self, ctx: SlashContext) -> None:
        sentences = [
            "**Fallen** on the horizon!",
            "**Vex** on the field!",
            "**Cabal** on the field!",
            "**Scorn** approaching!",
            "**Hive**! Bring a sword.",
        ]
        random = choice(sentences)

        if ctx.channel.id != warehouse_channel_id:
            warehouse_channel = await self.bot.fetch_channel(warehouse_channel_id)
            msg = await warehouse_channel.send(
                f"{ctx.author.mention} I think...\n{random}"
            )
            await ctx.send(f"I took my guess [here]({msg.jump_url})", ephemeral=True)
            return
        else:
            await ctx.send(f"I think...\n{random}")


def setup(bot: Client):
    Destiny(bot)
