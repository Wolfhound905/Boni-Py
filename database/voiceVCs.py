import os
import discord
from configuration import (get_user_name, get_password, get_user_name, get_host, get_database)
import mysql.connector



def get_voice_channels() -> list:
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    # Example: "custom_vc" is row[0]
    sql.execute(
        "SELECT custom_vc FROM voice_channels")
    rows = sql.fetchall()

    custom_vc = []

    for row in rows:
        custom_vc.append(row[0])
    return custom_vc
    sql.close()
    # If no rows exist then raise an error
    raise Exception("No rows in stats to read")

def add_vc(channel_id):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    sql.execute(f"""
    INSERT into voice_channels (custom_vc) values ({channel_id})
    """)
    sql.close()

def remove_vc(delete_vc):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    sql.execute(f"""
    DELETE FROM voice_channels WHERE custom_vc={delete_vc}
    """)
    sql.close()
