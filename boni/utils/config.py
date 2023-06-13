import re
from typing import List, Optional
from pydantic import BaseModel, root_validator, validator
from dotenv import dotenv_values
from boni.utils.logging import logger

__all__ = ("Config", "load_config")


class Discord(BaseModel):
    token: str
    """Discord Bot Token"""
    debug_scope: Optional[int] = None
    """Debug Scope"""

    birthday_channel_id: int

    @validator("token", "birthday_channel_id", pre=True)
    def required_fields(cls, v):
        if not v or v == "":
            raise ValueError("^^^ is required")
        return v


# # General config
# ROLES_RECRUIT=
# ROLES_SLAM=

# # Platforms
# ROLES_SWITCH=
# ROLES_PLAYSTATION=
# ROLES_XBOX=
# ROLES_PC=

# # Games
# ROLES_ROCKET_LEAGUE=
# ROLES_FORTNITE=
# ROLES_MINECRAFT=
# ROLES_HUNT_SHOWDOWN=

# # Regions
# ROLES_US_WEST=
# ROLES_US_CENTRAL=
# ROLES_US_EAST=
# ROLES_EU=
# ROLES_ASIA=


class Roles(BaseModel):
    recruit: int
    slam: int

    switch: int
    playstation: int
    xbox: int
    pc: int

    rocket_league: int
    fortnite: int
    minecraft: int
    hunt_showdown: int

    us_west: int
    us_central: int
    us_east: int
    eu: int
    asia: int

    @validator("*", pre=True)
    def required_fields(cls, v):
        if not v or v == "":
            raise ValueError("^^^ is required")
        return v


class MongoDB(BaseModel):
    host: str
    """Requires at least one host
    
    Example:
        host: inst1.example.com:27017,inst2.example.com:27017
    """
    database: str
    username: str
    password: str

    @validator("host", "username", "password", "database", pre=True)
    def required_fields(cls, v):
        if not v or v == "":
            raise ValueError("^^^ is required")
        return v


class Config(BaseModel):
    mongodb: MongoDB
    discord: Discord
    roles: Roles
    log_level: Optional[str] = "INFO"

    @validator("log_level")
    def log_level_is_valid(cls, v):
        if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(
                "Log level must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )
        return v


# NOTE: Below is code that loads the env and converts it to a Config object
def env_to_dict(keys: List[str]) -> dict:
    env_values = dotenv_values()
    if not env_values:
        import os

        env_values = os.environ.copy()

    env_dict = {}
    for key in keys:
        key_upper = key.upper()
        key_lower = key.lower()
        class_env_values = {
            k: (None if v == "" else v)
            for k, v in env_values.items()
            if k.startswith(key_upper)
        }
        class_env_values = {
            k.replace(key_upper + "_", "").lower(): v
            for k, v in class_env_values.items()
        }
        env_dict[key_lower] = class_env_values

    return env_dict


_config: Config = None


def load_config() -> Config:
    global _config
    if not _config:
        # classes = list of classes in this file that are subclasses of BaseModel
        keys = [
            cls.__name__
            for cls in globals().values()
            if isinstance(cls, type)
            and issubclass(cls, BaseModel)
            and cls is not BaseModel
            and cls is not Config
        ]

        config = env_to_dict(keys)

        _config = Config(**config)

    return _config
