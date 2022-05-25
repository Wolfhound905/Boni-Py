""" A temperary creation of a voice channel """

import naff
from boni.utils.rooms import add_room, del_room, get_rooms


class Rooms(naff.Extension):
    def __init__(self, bot: naff.Client):
        self.bot: naff.Client = bot

    @naff.slash_command(name="room", description="Create a voice channel")
    @naff.slash_option(
        "name", "What should the channel be called?", naff.OptionTypes.STRING, True
    )
    @naff.slash_option(
        "member_cap", "Set the member cap", naff.OptionTypes.INTEGER, False
    )
    async def room(
        self, ctx: naff.InteractionContext, name: str, member_cap: int = 0
    ) -> None:
        if not ctx.author.voice:
            await ctx.send("You have to be in a voice channel to use this command")
            return

        created_channel = await ctx.guild.create_voice_channel(
            name,
            category=ctx.author.voice.channel.parent_id,
            user_limit=member_cap,
            reason=f"Created by {ctx.author.username}",
        )
        await add_room(created_channel.id)

        await ctx.author.move(created_channel.id)

        await ctx.send(f"Created {created_channel.mention}!")

    @naff.listen(naff.events.VoiceStateUpdate)
    async def check_rooms(self, event: naff.events.VoiceStateUpdate):
        channel = event.before.channel if event.before else event.after.channel
        if channel.id not in await get_rooms():
            return
        channel: naff.GuildVoice = await self.bot.fetch_channel(channel.id)

        if len(channel.voice_members) == 0:
            await del_room(channel.id)
            await channel.delete()

    @naff.listen(naff.events.Startup)
    async def check_rooms_on_startup(self):
        # Check rooms to see if they are empty
        for room in await get_rooms():
            channel: naff.GuildVoice = await self.bot.fetch_channel(room)
            if not channel:
                await del_room(room)
                continue
            if len(channel.voice_members) == 0:
                await channel.delete()
                await del_room(channel.id)


def setup(bot: naff.Client):
    Rooms(bot)
