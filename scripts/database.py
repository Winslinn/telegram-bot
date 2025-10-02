import sqlite3, os

from telegram import Update

conn = sqlite3.connect(os.path.expanduser('~/bot/db/database.db'))
cur = conn.cursor()

def add_user(update: Update):
    user = update.message.from_user
    cur.execute('INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)', (user.id, user.username or user.full_name))
    conn.commit()

def user_subscribed(update: Update):
    cur.execute("""
    SELECT EXISTS(
        SELECT 1 FROM user_urls WHERE user_id = ?
    )
    """, (update.message.from_user.id,))
    
    return cur.fetchone()[0] == 1

def user_subscribe_url(user_id, url):
    if cur.execute('SELECT id FROM urls WHERE url = ?', (url,)).fetchone() is None:
        cur.execute('INSERT OR IGNORE INTO urls (url) VALUES (?)', (url,))
    
        cur.execute('SELECT id FROM urls WHERE url = ?', (url,))
        url_id = cur.fetchone()[0]
        
        cur.execute('INSERT OR IGNORE INTO user_urls (user_id, url_id) VALUES (?, ?)', (user_id, url_id))
        conn.commit()
    else:
        return False
    
def user_subscriptions(user_id):
    cur.execute("""
    SELECT urls.url FROM urls
    JOIN user_urls ON urls.id = user_urls.url_id
    WHERE user_urls.user_id = ?
    """, (user_id,))
    
    return [row[0] for row in cur.fetchall()]

def most_popular_urls(limit=5):
    cur.execute("""
    SELECT urls.url, COUNT(user_urls.user_id) as subscriber_count
    FROM urls
    JOIN user_urls ON urls.id = user_urls.url_id
    GROUP BY urls.id
    ORDER BY subscriber_count DESC
    LIMIT ?
    """, (limit,))
    
    return cur.fetchall()

def init_db():
    cur.execute('PRAGMA foreign_keys = ON')
    
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, rss_feed TEXT, title TEXT, genre TEXT)')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_urls (
            user_id INTEGER,
            url_id INTEGER,
            PRIMARY KEY (user_id, url_id),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE, 
            FOREIGN KEY(url_id) REFERENCES urls(id) ON DELETE CASCADE
        )
    ''')
    
    return conn, cur