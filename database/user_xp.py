import os
import discord
from configuration import (get_user_name, get_password, get_user_name, get_host, get_admins, get_database)
import mysql.connector

# Using this class as return type for get_stats function


def get_xp(user_id: str):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    
    sql.execute(f"""
        SELECT SUM(xp) from user_xp
        WHERE user_id = {user_id}""")
    xp = sql.fetchone()[0]
    sql.close()
    
    return xp


def get_recent_xp(user_id: str):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    
    sql.execute(f"""
        SELECT SUM(xp) from user_xp
        WHERE user_id = {user_id} AND timestamp BETWEEN (NOW() - INTERVAL 14 DAY) AND NOW()""")
    xp = sql.fetchone()[0]
    sql.close()
    
    return xp


def add_xp(user_id: int, xp: int):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    
    sql.execute(f"""
    INSERT INTO user_xp
        (user_id, timestamp, xp)
    VALUES
        ({user_id}, NOW(), {xp});
    """)
    
    db.commit()
    sql.close()

