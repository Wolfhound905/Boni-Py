import psycopg2
import os

db = os.getenv('DB')

#Using this class as return type for get_stats function
class Stats():
    win = 0
    losses = 0 
    win_streak = 0
    loss_streak = 0

    def __init__(self, win, loses, win_streak, loss_streak):
        self.win = win
        self.losses = loses
        self.win_streak = win_streak
        self.loss_streak = loss_streak

def get_stats() -> Stats:
    con = psycopg2.connect(db)
    cur = con.cursor()
    # Example: "wins" is row[0]
    cur.execute(
        "SELECT wins, losses, win_streak, loss_streak from stats")
    rows = cur.fetchall()

    for row in rows:
        return Stats(row[0], row[1], row[2], row[3])
    
    #If no rows exist then raise an error
    raise Exception("No rows in stats to read")


def increment_win():
    con = psycopg2.connect(db)
    cur = con.cursor()
    cur.execute(
        """UPDATE stats SET
            wins = wins + 1, 
            win_streak = win_streak + 1,
            loss_streak= 0""")
    con.commit()
    con.close()

def increment_loss():
    con = psycopg2.connect(db)
    cur = con.cursor()
    cur.execute(
        """UPDATE stats SET
            losses = losses + 1, 
            win_streak = 0,
            loss_streak= loss_streak + 1""")
    con.commit()
    con.close()