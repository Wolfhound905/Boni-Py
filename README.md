#  ↗![icon](https://cdn.discordapp.com/avatars/819606905735479356/d9a465142e9caf564de77f1eebec4103.png?size=256)↖ Boni-Py
Boni-Py is a discord bot for the one and only Slambonis server. Although he may look simple, there is a few things going on under that hood of his. He can create temperary voice channels and uses Discords new slash commands to the best of there abilities.

## How to use
To run this project you need discord.py and slash commands

There is a `sample.env` that you must fill out and rename to `.env`

## Migrations (yoyo-migrations)
To use migrations start by downloading the necessary packages first
`pip install -r requirements-dev.txt`

Then create the yoyo configuration file `yoyo.ini` in the base directory and fill it with the following

    [DEFAULT]
    sources = ./migrations/
    database = mysql://{user}@{host}/{database}
    migration_table = _yoyo_migration
    batch_mode = off
    verbosity = 0
    
From there you can apply and rollback existing migrations
`yoyo apply -p`
`yoyo rollback -p`
Or create a new migration with
`yoyo new -m "migration name"`


### 🚧 This read me is still being made 🚧

