import naff
from random import choice


class Destiny(naff.Extension):
    def __init__(self, bot: naff.Snake):
        self.bot: naff.Snake = bot

    @naff.slash_command(name="gambit", description="Who we versing?")
    async def gambit(self, ctx: naff.InteractionContext) -> None:
        sentences = [
            "**Fallen** on the horizon!",
            "**Vex** on the field!",
            "**Cabal** on the field!",
            "**Scorn** approaching!"
        ]

        await ctx.send(f"I think...\n{choice(sentences)}")


def setup(bot: naff.Snake):
    Destiny(bot)
