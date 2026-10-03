import sqlite3

DB = 'library.db'

def add_book(isbn, title, author, location, issue_date='', subtitle=''):
    conn = sqlite3.connect(DB)
    try:
        conn.execute(
            "INSERT INTO books(isbn, title, author, location, issue_date, subtitle) "
            "VALUES(?, ?, ?, ?, ?, ?)",
            (isbn, title, author, location, issue_date, subtitle)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def search_book(keyword):
    conn = sqlite3.connect(DB)
    cur = conn.execute(
        """
        SELECT isbn, title, author, location 
        FROM books
        WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
        """,
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("没有找到匹配的书。")
        return

    for isbn, title, author, location in rows:
        print(f"《{title}》 {author} | ISBN:{isbn} | 位置：{location}")

def update_book(isbn, field, new_value):
    conn = sqlite3.connect(DB)
    try:
        conn.execute(
            f"UPDATE books SET {field} = ? WHERE isbn = ?",
            (new_value, isbn)
        )
        conn.commit()
        return conn.total_changes > 0
    finally:
        conn.close()

def delete_book(isbn):
    conn = sqlite3.connect(DB)
    try:
        conn.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        conn.commit()
        return conn.total_changes > 0
    finally:
        conn.close()

def book_exists(isbn):
    conn = sqlite3.connect(DB)
    cur = conn.execute("SELECT 1 FROM books WHERE isbn = ?", (isbn,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def main():
    while True:
        print("\n=== Rosalyn的个人图书馆 ===")
        print("1. 添加书")
        print("2. 搜索书")
        print("3. 修改书")
        print("4. 删除书")
        print("5. 退出")
        choice = input("请选择：").strip()

        if choice == '1':
            isbn = input("ISBN:").strip()
            title = input("书名：").strip()
            author = input("作者：").strip()
            location = input("位置（如 书房A-3）：").strip()
            if add_book(isbn, title, author, location):
                print(f"已添加:《{title}》")
            else:
                print(f"重复！ISBN{isbn}已存在，未添加。")

        elif choice == '2':
            keyword = input("关键词：").strip()
            search_book(keyword)

        elif choice == '3':
            isbn = input("要修改的书的 ISBN：").strip()
            if not book_exists(isbn):
                print(f"没有找到 ISBN 为 {isbn} 的书。")
                continue
            print("可改字段：1.书名 2.作者 3.位置")
            f = input("选哪个：").strip()
            field_map ={"1": "title", "2": "author", "3": "location"}
            if f not in field_map:
                print("无效字段。")
                continue
            new_value = input("新内容：").strip()
            if update_book(isbn, field_map[f], new_value):
                print("已修改。")
            else:
                print("修改失败。")

        elif choice == '4':
            isbn = input("要删除的书的 ISBN：").strip()
            if not book_exists(isbn):
                print(f"没有找到 ISBN 为 {isbn} 的书。")
                continue
            confirm = input(f"确认删除 ISBN{isbn}？（y/n）：").strip().lower()
            if confirm == 'y':
                if delete_book(isbn):
                    print(f"已删除 ISBN：{isbn}")
                else:
                    print("删除失败。")
            else:
                print("已取消。")

        elif choice == '5':
            print("感谢使用，再见。")
            break

        else:
            print("无效选择，请重试。")

if __name__ == "__main__":
    main()