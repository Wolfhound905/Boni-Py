from types import NoneType
from typing import List
from boni.db.models.rooms import Rooms


async def add_room(channel_id: int) -> NoneType:
    """Add a room"""
    await Rooms(channel_id=channel_id).save()


async def del_room(channel_id: int) -> NoneType:
    """Delete a room"""

    await Rooms.find({"channel_id": channel_id}).delete()


async def get_rooms() -> List[int]:
    """Get all rooms"""
    return [room.channel_id for room in await Rooms.find().to_list()]
