import asyncio
import naff
from datetime import timedelta

from boni.utils.rocket_league import Tournament, get_tourneys


class RocketLeague(naff.Extension):
    def __init__(self, bot: naff.Client):
        self.bot: naff.Client = bot

    rl_base_cmd = naff.SlashCommand(name="rocket_league", description="Rocket League commands")

    @rl_base_cmd.subcommand(
        sub_cmd_name="tourneys", sub_cmd_description="Get upcoming tourneys"
    )
    @naff.slash_option(
        "region",
        description="Effects what tourneys are show",
        opt_type=naff.OptionTypes.STRING,
        required=False,
        choices=[
            naff.SlashCommandChoice("Europe", "EU"),
            naff.SlashCommandChoice("US", "USE"),
        ],
    )
    async def tourneys(self, ctx: naff.InteractionContext, region: str = "USE") -> None:
        tourneys = await get_tourneys(region)
        embed = naff.Embed(
            title="Rocket League Tourneys",
            color="#0099ff",
            thumbnail="https://cdn.discordapp.com/attachments/819980437329543180/981374008031330354/unknown.png",
        )

        select_options = []
        for tourney in tourneys[:5]:
            time_str = tourney.timestamp.strftime("%I:%M %p")
            select_options.append(
                naff.SelectOption(
                    tourney.name, str(tourney.timestamp.timestamp()), time_str
                )
            )
            start_time = tourney.timestamp.format(naff.TimestampStyles.ShortTime)
            relative_time = tourney.timestamp.format(naff.TimestampStyles.RelativeTime)
            embed.add_field(
                name=tourney.name,
                value=f"Starts at {start_time} ({relative_time})",
                inline=False,
            )

        select = naff.Select(select_options, placeholder="Sign me up for a tourney!")
        sent = await ctx.send(embed=embed, components=select)

        try:
            select_resp = await self.bot.wait_for_component(
                components=select,
                timeout=60,
                check=lambda x: x.context.author.id == ctx.author.id,
            )
            await self.handle_tourney_select(select_resp.context, tourneys)

        except asyncio.TimeoutError:
            disabled = naff.Select(
                select_options, placeholder="Run the command again!", disabled=True
            )
            await sent.edit(components=disabled)

    async def handle_tourney_select(
        self, ctx: naff.ComponentContext, tourneys: list
    ) -> None:
        selected: "Tournament" = [
            tourney
            for tourney in tourneys
            if str(tourney.timestamp.timestamp()) == ctx.values[0]
        ][0]
        event = await ctx.guild.create_scheduled_event(
            f"Rocket League {selected.name} Tourney",
            event_type=naff.ScheduledEventType.EXTERNAL,
            start_time=selected.timestamp - timedelta(minutes=15),
            description=f"{ctx.author.mention} wants to play a {selected.name} tourney! Sign up to get notified before it starts!",
            external_location=f"{selected.name} {selected.timestamp.format(naff.TimestampStyles.RelativeTime)}",
            end_time=selected.timestamp + timedelta(minutes=15),
            cover_image=await selected.image_bytes()
        )
        event_invite = f"https://discord.com/events/{ctx.guild.id}/{event.id}"

        await ctx.edit_origin(
            f"<@&698631135919341599> | {ctx.author.mention} wants to play in a tourney.\n Here is [event]({event_invite}) to remind you. Make sure to click **Interested**!",
            components=[],
            embed=[],
        )


def setup(bot: naff.Client):
    RocketLeague(bot)
