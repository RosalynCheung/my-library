import streamlit as st
import sqlite3

from library import add_book, delete_book, update_book

st.title("Rosalyn's Library")

with st.expander("➕️ 添加新书"):
    with st.form("add_book_form"):
        isbn = st.text_input("ISBN")
        title = st.text_input("书名")
        author = st.text_input("作者")
        location = st.text_input("位置（如 书房-A-3")
        issue_date = st.text_input("期刊（杂志才填，如 20260706）")
        subtitle = st.text_input("封面故事主题（杂志才填）")

        submitted = st.form_submit_button("添加")

        if submitted:
            if not isbn or not title:
                st.error("ISBN 和书名必填。")
            else:
                ok = add_book(isbn, title, author, location, issue_date, subtitle)
                if ok:
                    st.toast(f"已添加：《{title}》", icon="✅️")
                else:
                    st.toast(f"重复！ISBN{isbn}已存在，未添加。", icon="⚠️")


keyword = st.text_input("搜索书名 / 作者 / ISBN / 主题")

conn = sqlite3.connect("library.db")

if keyword:
    rows = conn.execute(
        """
        SELECT title, author, location, issue_date, subtitle, isbn 
        FROM books
        WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
           OR subtitle LIKE ? OR issue_date LIKE ?
        """,
        (f"%{keyword}%",) * 5
    ).fetchall()
else:
    rows = conn.execute(
        "SELECT title, author, location, issue_date, subtitle, isbn FROM books"
    ).fetchall()

conn.close()

st.write(f"共 {len(rows)} 本书")

for title, author, location, issue_date, subtitle, isbn in rows:
    col1, col2, col3 = st.columns([5, 1, 1])

    with col1:
        if issue_date:
            st.write(f"《{title}》 {issue_date}期 · {subtitle} | ISBN: {isbn} | 位置： {location}")
        else:
            st.write(f"《{title}》 {author} | ISBN: {isbn} | 位置：{location}")

    with col2:
        if st.button("编辑", key=f"edit_{isbn}"):
            st.session_state.edit_target = isbn
            st.session_state.edit_issue_date = issue_date

    with col3:
        if st.button("删除", key=f"del_{isbn}"):
            st.session_state.delete_target = isbn

if "edit_target" in st.session_state and st.session_state.edit_target:
    target = st.session_state.edit_target
    st.info(f"正在编辑 ISBN 为{target} 的书")

    is_magazine = bool(st.session_state.edit_issue_date)
    if is_magazine:
        field_map = {"书名": "title", "作者": "author", "ISBN": "isbn", "位置": "location", "刊期": "issue_date", "主题": "subtitle"}
    else:
        field_map = {"书名": "title", "作者": "author", "ISBN": "isbn", "位置": "location"}

    with st.form("edit_form"):
        field_label = st.selectbox("选择修改字段", list(field_map.keys()))
        new_value = st.text_input("新内容")
        submitted = st.form_submit_button("提交修改")

        if submitted:
            if not new_value:
                st.error("新内容不能为空。")
            else:
                ok = update_book(target, field_map[field_label], new_value)
                if ok:
                    st.toast("已修改。", icon='✅️')
                else:
                    st.toast("修改失败。", icon='⚠️')
                st.session_state.edit_target = None
                st.rerun()

    if st.button("取消编辑"):
        st.session_state.edit_target = None
        st.session_state.edit_issue_date = None
        st.rerun()

if "delete_target" in st.session_state and st.session_state.delete_target:
    target = st.session_state.delete_target
    st.warning(f"确认删除 ISBN 为 {target} 的书？")

    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("确认删除"):
            if delete_book(target):
                st.toast("已删除。", icon='✅️')
            else:
                st.toast("删除失败。", icon='⚠️')
            st.session_state.delete_target = None
            st.rerun()

    with col_no:
        if st.button("取消"):
            st.session_state.delete_target = None
            st.rerun()