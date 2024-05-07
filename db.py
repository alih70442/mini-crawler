import sqlite3

DB_TYPE_ENAMAD_SITE = 0
DB_TYPE_TAPIN_PODRO_SITE = 1

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
    
def clear_type(type):
    conn = sqlite3.connect('data.db')

    cursor = conn.cursor()

    sql = f"DELETE FROM crawls WHERE type = {type}"
    cursor.execute(sql)

    conn.commit()

    conn.close()

def fetch_custom_sql (sql):
    conn = sqlite3.connect('data.db')

    cursor = conn.cursor()

    cursor.execute(sql)

    data = cursor.fetchall()

    conn.close()
    
    return data
