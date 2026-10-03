import sqlite3

conn = sqlite3.connect("library.db")

conn.execute("""
    CREATE TABLE IF NOT EXISTS books(
        isbn TEXT UNIQUE,
        title TEXT,
        author TEXT,
        location TEXT
    )
""")

conn.commit()
conn.close()
