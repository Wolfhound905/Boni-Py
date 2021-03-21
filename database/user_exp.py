import os
import discord
from configuration import (get_user_name, get_password, get_user_name, get_host, get_admins, get_database)
import mysql.connector

# Using this class as return type for get_stats function


def get_stats() -> Stats:
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    # Example: "season" is row[0]
    sql.execute(
        "SELECT season, wins, losses, win_streak, loss_streak, max_win_streak, max_loss_streak from stats WHERE season = (SELECT Max(season) FROM stats)")
    rows = sql.fetchall()

    for row in rows:
        return Stats(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    sql.close()

    # If no rows exist then raise an error
    raise Exception("No rows in stats to read")


def user_exp(member_id, give):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    stats = get_stats()
    season = str(stats.season)
    new_max_win_streak = str(max(stats.win_streak + 1, stats.max_win_streak))
    sql.execute(f"""
    UPDATE stats
    SET wins = wins + 1, loss_streak = 0, win_streak= win_streak + 1, max_win_streak= {new_max_win_streak}
    WHERE season = {season}
    """)
    sql.close()

