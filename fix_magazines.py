import sqlite3

conn = sqlite3.connect('library.db')

conn.execute(
    "UPDATE books SET isbn = ?, title = ?, issue_date = ?, subtitle = ? WHERE title LIKE ?",
    ("977100536026027", "三联生活周刊", "20260706", "沿着湄公河", "%20260706%")
)

conn.execute(
    "UPDATE books SET isbn = ?, title = ?, issue_date = ?, subtitle = ? WHERE title LIKE ?",
    ("977100536026028", "三联生活周刊", "20260713", "夏日阅读", "%20260713%")
)

conn.commit()
conn.close()

print("两本杂志已修正。")