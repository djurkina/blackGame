import sqlite3
import settings

def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 100
        )
    ''')
    conn.commit()

def get_user_balance(conn, user_id):
    cursor = conn.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else 100

def update_user_balance(conn, user_id, amount):
    conn.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
    conn.commit()

def add_user(conn, user_id):
    conn.execute("INSERT OR IGNORE INTO users (id, balance) VALUES (?, ?)", (user_id, 100))
    conn.commit()

def get_conn():
    return sqlite3.connect(settings.DATABASE_FILE)
