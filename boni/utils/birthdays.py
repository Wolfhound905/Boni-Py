from datetime import datetime
from types import NoneType
from typing import List

from boni.db.models import Birthdays


async def insert_bday(user_id: int, date: datetime) -> NoneType:
    """Insert birthday into db"""

    if existing := await get_bday(user_id):
        existing.birthday = date
        await existing.save()
    else:
        await Birthdays(user_id=user_id, birthday=date).save()


async def reply_bday(user_id: int) -> NoneType:
    """Add the data that the reply was made"""

    if existing := await get_bday(user_id):
        existing.last_replied = datetime.now()
        await existing.save()


async def get_all_bdays() -> List[Birthdays]:
    """Get all birthdays"""

    return await Birthdays.find().to_list()


async def get_bday(user_id: int) -> Birthdays:
    """Get birthday"""

    return await Birthdays.find_one({"user_id": user_id})
