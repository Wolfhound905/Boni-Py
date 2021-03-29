import os
import discord
from configuration import (get_user_name, get_password, get_user_name, get_host, get_admins, get_database)
import mysql.connector

# Using this class as return type for get_stats function


def add_match(match: bool, player_1: discord.Member, player_2: discord.Member, player_3: discord.Member = None, player_4: discord.Member = None, overtime: bool = None):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    sql.execute("""
    INSERT INTO matches
    (win, overtime, match_time)
    VALUES(%s, %s, CURRENT_TIMESTAMP)
    """, (match, overtime))

    match_id = sql.lastrowid
    match_query = ("""
    INSERT INTO users_matches
    (user_id, match_id)
    VALUES(%s, %s), (%s, %s)
    """)
    match_data = [player_1.id, match_id, player_2.id, match_id]
    if player_3 is not None:
        match_query = match_query + ",(%s, %s)"
        match_data.extend([player_3.id, match_id])

    if player_4 is not None:
        match_query = match_query + ",(%s, %s)"
        match_data.extend([player_4.id, match_id])

    print(match_query)
    print(match_data)
    sql.execute(match_query, tuple(match_data))
    db.commit()
    sql.close()

def get_guild_stats(id: int = None):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    season_id = id if id is not None else "(SELECT Max(id) FROM seasons)"

    sql.execute(f"""
    SELECT matches.* FROM seasons
    INNER JOIN matches on matches.match_time >= seasons.date_start and matches.match_time <= seasons.date_end
    WHERE seasons.id = {season_id}
    """)
    rows = sql.fetchall()

    wins = len([x for x in rows if x[1] == 1])
    losses = len([x for x in rows if x[1] == 0])

    sql.close()
