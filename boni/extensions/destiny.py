import naff
from random import choice

warehouse_channel_id = 819980437329543180


class Destiny(naff.Extension):
    def __init__(self, bot: naff.Client):
        self.bot: naff.Client = bot

    @naff.slash_command(name="gambit", description="Who we versing?")
    async def gambit(self, ctx: naff.InteractionContext) -> None:
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


def setup(bot: naff.Client):
    Destiny(bot)
