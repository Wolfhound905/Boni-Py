""" Database Models """

from .birthdays import Birthdays
from .rooms import Rooms


__beanie_models__ = [Birthdays, Rooms]
