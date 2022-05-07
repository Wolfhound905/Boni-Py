from typing import Optional
from beanie import Document, Indexed
from datetime import datetime


class Birthdays(Document):
    """Opted Out Model"""

    user_id: Indexed(int, unique=True)
    birthday: datetime
    last_replied: Optional[datetime] = None
    """ The data of the reply """
