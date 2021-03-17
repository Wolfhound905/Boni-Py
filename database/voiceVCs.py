import os
import discord
from configuration import (get_user_name, get_password,
                           get_user_name, get_host, get_database)
import mysql.connector

db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
sql = db.cursor()



def get_voice_channels() -> list:
    # Example: "active_vc" is row[0]
    sql.execute(
        "SELECT active_vc FROM voice_channels")
    rows = sql.fetchall()

    active_vcs = []

    for row in rows:
        active_vcs.append(row[0])
    return active_vcs

    # If no rows exist then raise an error
    raise Exception("No rows in stats to read")

def add_vc(channel_id):
    sql.execute(f"""
    INSERT into voice_channels (active_vc) values ({channel_id})
    """)
    sql.close()

def remove_vc(delete_vc):
    sql.execute(f"""
    DELETE FROM voice_channels WHERE active_vc={delete_vc}
    """)
    sql.close()
