import sqlite3

conn = sqlite3.connect('library.db')

conn.execute('ALTER TABLE books ADD COLUMN issue_date TEXT')
conn.execute('ALTER TABLE books ADD COLUMN subtitle TEXT')

conn.commit()
conn.close()

print("已加两列： issue_date、subtitle")