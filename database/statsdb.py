import os
import discord
from configuration import (get_user_name, get_password,
                           get_user_name, get_host, get_admins, get_database)
import mysql.connector
from itertools import groupby
from typing import Tuple

# Using this class as return type for get_stats function

def update_users(guild_members):
    db = mysql.connector.connect(user=get_user_name(
    ), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()

    for Member in guild_members:
        if not Member.bot:
            sql.execute(f"""
            REPLACE INTO users(id, name, avatar_url) values("{Member.id}", "{Member.name}", "{Member.avatar_url}")
            """)
    db.commit()
    sql.close()



def add_match(match: bool, player_1: discord.Member, player_2: discord.Member, player_3: discord.Member = None, player_4: discord.Member = None, overtime: bool = None):
    db = mysql.connector.connect(user=get_user_name(
    ), password=get_password(), host=get_host(), database=get_database())
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
    VALUES(%s, %s)
    """)

    members_list = []
    members_list.append(player_1.id)
    members_list.append(player_2.id)
    if player_3 is not None:
        members_list.append(player_3.id)
    if player_4 is not None:
        members_list.append(player_4.id)
    members_list = list(set(members_list))

    match_data = []

    for x in members_list:
        match_data.append(x)
        match_data.append(match_id)
        if len(match_data) > 2:
            match_query = match_query + ",(%s, %s)"

    sql.execute(match_query, match_data)

    db.commit()
    sql.close()


def get_guild_stats(id: int = None):
    db = mysql.connector.connect(user=get_user_name(
    ), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    season_id = id if id is not None else "(SELECT Max(id) FROM seasons WHERE CURRENT_TIMESTAMP >= seasons.date_start and CURRENT_TIMESTAMP <= seasons.date_end)"

    sql.execute(f"""
    SELECT matches.*, seasons.number FROM seasons
    INNER JOIN matches on matches.match_time >= seasons.date_start and matches.match_time <= seasons.date_end
    WHERE seasons.id = {season_id}
    """)
    rows = sql.fetchall()
    sql.close()

    stats = stats_transform(rows) if rows != [] else None

    return(stats)

def get_user_stats(uid, sid: int = None):
    db = mysql.connector.connect(user=get_user_name(
    ), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    season_id = sid if sid is not None else "(SELECT Max(id) FROM seasons WHERE CURRENT_TIMESTAMP >= seasons.date_start and CURRENT_TIMESTAMP <= seasons.date_end)"

    sql.execute(f"""
    SELECT matches.*, seasons.number as season, users_matches.user_id FROM seasons
    INNER JOIN matches on matches.match_time >= seasons.date_start and matches.match_time <= seasons.date_end
    INNER JOIN users_matches ON users_matches.match_id = matches.id
    WHERE seasons.id = {season_id}
    AND users_matches.user_id = {uid}
    """)

    rows = sql.fetchall()
    sql.close()

    stats = stats_transform(rows) if rows != [] else None

    return(stats)
    

def stats_transform(rows):
    season = rows[0][4]
    wins = len([row for row in rows if row[1]])
    losses = len([row for row in rows if not row[1]])

    match_result = [x[1] for x in rows]

    streaks = [(1,0), (0,0)] # Default vaules for no wins and no losses
    streaks += [(key, len(list(group))) for key, group in groupby(match_result)]

    win_streak = max([x for x in streaks if x[0] == 1], key=lambda x: x[1])[1]
    loss_streak = max([x for x in streaks if x[0] == 0], key=lambda x: x[1])[1]
    current_streak = streaks[-1]

    stats = {
        "wins": wins,
        "losses": losses,
        "win_streak": win_streak,
        "loss_streak": loss_streak,
        "current_streak": current_streak,
        "season": season
    }

    return(stats)
