import sqlite3, os, json

from telegram import Update

conn = sqlite3.connect(os.path.expanduser('~/bot/db/database.db'))
cur = conn.cursor()

def add_user(update: Update):
    user = update.message.from_user
    cur.execute('INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)', (user.id, user.username or user.full_name))
    conn.commit()

def check_user(update: Update):
    cur.execute('SELECT id FROM users WHERE id = ?', (update.message.from_user.id,))
    return cur.fetchone()

def init_db():
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS urls (urls TEXT PRIMARY KEY, user_id INTEGER)')
    return conn, cur