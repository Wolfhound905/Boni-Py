import os
import discord
from configuration import (get_user_name, get_password, get_user_name, get_host, get_admins, get_database, get_guilds)
import mysql.connector

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


async def add_xp(user_id: int, xp: int, bot):
    old_xp = get_recent_xp(user_id)
    if old_xp + xp > 2000:
        await add_reward(bot, user_id)

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

async def add_reward(bot, user_id: int):
    for member in bot.get_all_members():
        print(f"{member.guild.id} has {member.id}")
        if member.guild.id in get_guilds() and member.id == user_id:
            print("Tries to add role")
            role = get(member.server.roles, name="name of role")
            await bot.add_roles(member, role)

async def remove_reward(bot, user_id: int):
    print(f"Remove reward for player {user_id}")