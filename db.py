import sqlite3

def init():
    conn = sqlite3.connect('data.db')

    cursor = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS crawls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value TEXT NOT NULL,  -- Consider using a specific crawls type for JSON if applicable
                type BIGINT NOT NULL
            )"""
    cursor.execute(sql)

    conn.commit()

    conn.close()

    print("Database is connected")
    
def insert(value, type):
    conn = sqlite3.connect('data.db')

    cursor = conn.cursor()

    sql = """INSERT INTO crawls (value, type) VALUES (?, ?)"""
    cursor.execute(sql, (value, type))

    conn.commit()

    conn.close()

def fetch(type):
    conn = sqlite3.connect('data.db')

    cursor = conn.cursor()

    sql = f"SELECT * FROM crawls WHERE type = {type}" 
    cursor.execute(sql)

    data = cursor.fetchall()

    conn.close()
    
    return data
    
