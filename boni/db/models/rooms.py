from beanie import Document, Indexed


class Rooms(Document):
    """Opted Out Model"""

    channel_id: Indexed(int, unique=True)
