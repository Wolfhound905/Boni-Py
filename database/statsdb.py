import psycopg2
import os
import discord
from configuration import get_db

db = get_db()

# Using this class as return type for get_stats function
class Stats():
    season = 0
    win = 0
    losses = 0
    win_streak = 0
    loss_streak = 0
    max_win_streak = 0
    max_loss_streak = 0

    def __init__(self, season, wins, losses, win_streak, loss_streak, max_win_streak, max_loss_streak):
        self.season = season
        self.wins = wins
        self.losses = losses
        self.win_streak = win_streak
        self.loss_streak = loss_streak
        self.max_win_streak = max_win_streak
        self.max_loss_streak = max_loss_streak


def get_stats() -> Stats:
    con = psycopg2.connect(db)
    cur = con.cursor()
    # Example: "season" is row[0]
    cur.execute(
        "SELECT season, wins, losses, win_streak, loss_streak, max_win_streak, max_loss_streak from stats WHERE season = (SELECT Max(season) FROM stats)")
    rows = cur.fetchall()

    for row in rows:
        return Stats(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    # If no rows exist then raise an error
    raise Exception("No rows in stats to read")


def increment_win():
    con = psycopg2.connect(db)
    cur = con.cursor()
    cur.execute("""
    UPDATE stats
    SET wins = wins + 1, loss_streak = 0, win_streak= win_streak + 1, max_win_streak= (SELECT Greatest(max_win_streak, win_streak + 1) FROM stats WHERE season = (SELECT Max(season) FROM stats))
    WHERE season = (SELECT Max(season) FROM stats)
    """)
    con.commit()
    con.close()


def increment_loss():
    con = psycopg2.connect(db)
    cur = con.cursor()
    cur.execute("""
    UPDATE stats
    SET losses = losses + 1, win_streak = 0, loss_streak= loss_streak + 1, max_loss_streak= (SELECT Greatest(max_loss_streak, loss_streak + 1) FROM stats WHERE season = (SELECT Max(season) FROM stats))
    WHERE season = (SELECT Max(season) FROM stats)
    """)
    con.commit()
    con.close()


def increment_new_season(season):
    con = psycopg2.connect(db)
    cur = con.cursor()
    cur.execute(
        f"""INSERT INTO stats 
        (season, wins, losses, win_streak, loss_streak, max_win_streak, max_loss_streak) 
        VALUES({season}, 0, 0, 0, 0, 0, 0)
        """)
    con.commit()
    con.close()
