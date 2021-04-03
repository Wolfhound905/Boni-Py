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

async def check_for_reward_removal(bot: discord.Client):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()

    sql.execute("""
        SELECT user_id, SUM(xp)
        FROM user_xp
        WHERE timestamp BETWEEN (NOW() - INTERVAL 14 DAY) AND NOW()
        GROUP BY user_id""")
    for (user_id, total_xp) in sql.fetchall():
        if total_xp < 1000:
            await remove_reward(bot, user_id)

async def add_xp(user_id: int, xp: int, bot: discord.Client):
    old_xp = get_recent_xp(user_id)
    if old_xp is not None:
        if old_xp + xp >= 2000:
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

async def add_reward(bot: discord.Client, user_id: int):
    guild = bot.get_guild(443884809484238848)
    member = guild.get_member(user_id)
    role = guild.get_role(825434367391170631)
    await member.add_roles(role)

async def remove_reward(bot: discord.Client, user_id: int):
    guild = bot.get_guild(443884809484238848)
    member = guild.get_member(user_id)
    role = guild.get_role(825434367391170631)
    await member.remove_roles(role)