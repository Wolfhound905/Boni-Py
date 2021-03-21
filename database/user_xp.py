import os
import discord
from configuration import (get_user_name, get_password, get_user_name, get_host, get_admins, get_database)
import mysql.connector

# Using this class as return type for get_stats function


def get_xp(user_id: str):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    # Example: "season" is row[0]
    sql.execute(
        f"SELECT xp from user_xp WHERE user_id = {user_id}")
    rows = sql.fetchall()
    sql.close()
    for row in rows:
        return (row[0])
    return 0


def add_xp(user_id: str, give: str):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    sql.execute(f"""
    INSERT IGNORE INTO user_xp
        (user_id, xp)
    VALUES
        ({user_id}, 0);
    """)
    sql.execute(f"""
    UPDATE user_xp
    SET xp = xp + {give}
    WHERE user_id = {user_id}
    """)

    sql.close()

