import json
from random import choice
import dis_snek as dis
from datetime import datetime
from asyncio import TimeoutError

from dotenv import get_key

from boni.utils.birthdays import insert_bday, get_bday, get_all_bdays, reply_bday

with open("./boni/utils/birthday_messages.json") as f:
    birthday_messages = json.load(f)


class Birthdays(dis.Scale):
    def __init__(self, bot: dis.Snake):
        self.bot: dis.Snake = bot
        self.bday_channel_id: int = int(get_key(".env", "BIRTHDAY_CHANNEL_ID"))

    @dis.slash_command(name="birthday")
    async def birthday(self) -> None:
        ...

    # NOTE: this is just to set the base birthday command

    @birthday.subcommand("set")
    @dis.slash_option(
        "birthday",
        "Make sure to format your birthday as MM/DD/YYYY (3/11/2021)",
        dis.OptionTypes.STRING,
        True,
    )
    async def birthday_set(self, ctx: dis.InteractionContext, birthday: str) -> None:
        try:
            date_time_obj = datetime.strptime(birthday, "%m/%d/%Y")
        except ValueError:
            await ctx.send("Invalid date format. Please use MM/DD/YYYY")
            return

        age = (datetime.now() - date_time_obj).days // 365
        str_date = date_time_obj.strftime("%B %d, %Y")

        if age < 10:
            await ctx.send(
                "Uhm, are you sure you are that young? Maybe you entered your birthday wrong?"
            )
            return

        confirm_btns = [
            dis.Button(
                dis.ButtonStyles.GREEN,
                "Looks good!",
                custom_id=f"bday_confirm.{ctx.author.id}.{birthday}",
            ),
            dis.Button(
                dis.ButtonStyles.RED, "Nah", custom_id=f"bday_cancel.{ctx.author.id}"
            ),
        ]

        await ctx.send(
            f"So you where born on {str_date}?\nMeaning you are {age} years old?",
            components=[confirm_btns],
        )

    @dis.listen(dis.events.Button)
    async def check_bday(self, event: dis.events.Button) -> None:
        btn_ctx = event.context
        if event.context.custom_id.startswith("bday_confirm"):
            data = event.context.custom_id.split(".")
            if data[1] == str(btn_ctx.author.id):
                date_time_obj = datetime.strptime(data[2], "%m/%d/%Y")
                await insert_bday(btn_ctx.author.id, date_time_obj)
                await event.context.edit_origin(
                    "Great! I'll remember that!", components=[]
                )
                return
            else:
                await btn_ctx.send("This is not your button to click.", ephemeral=True)
                return
        else:
            data = event.context.custom_id.split(".")
            if data[1] == str(btn_ctx.author.id):
                await event.context.edit_origin("Alrighty.", components=[])
                return
            else:
                await btn_ctx.send("This is not your button to click.", ephemeral=True)
                return

    @dis.Task.create(dis.IntervalTrigger(days=1))
    async def check_bday_task(self) -> None:
        """Check if any users have a birthday today"""
        bdays = await get_all_bdays()

        user_ids_with_bday = [
            bday.user_id
            for bday in bdays
            if bday.birthday.day == datetime.now().day
            and (
                bday.last_replied.year != datetime.now().year
                if bday.last_replied
                else True
            )
        ]

        if len(user_ids_with_bday) == 0:
            return

        channel = await self.bot.fetch_channel(self.bday_channel_id)

        if len(user_ids_with_bday) == 1:
            await channel.send(
                choice(birthday_messages).replace(
                    "{user}", f"<@{user_ids_with_bday[0]}>"
                )
            )
            await reply_bday(user_ids_with_bday[0])
            return
        elif len(user_ids_with_bday) > 1:
            users = " and ".join([f"<@{user_id}>" for user_id in user_ids_with_bday])
            await channel.send(
                (choice(birthday_messages)).replace("{user}", str(users))
            )
            [await reply_bday(user_id) for user_id in user_ids_with_bday]
            return

    @dis.listen(dis.events.Startup)
    async def on_startup(self) -> None:
        await self.check_bday_task()
        self.check_bday_task.start()


def setup(bot: dis.Snake):
    Birthdays(bot)
