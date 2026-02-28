import streamlit as st
from model import get_all_books
from controller import (
    save_book_controller,
    reset_book_form,
    delete_book_controller,
    update_book_controller
)

def render_book_page():
    """ฟังก์ชันหลักสำหรับหน้าจัดการหนังสือ"""
    st.header("📚 จัดการข้อมูลหนังสือ")
    
    # --- ส่วนที่ 1: เพิ่มข้อมูลหนังสือใหม่ ---
    render_add_book_section()
    st.divider()

    # --- ส่วนที่ 2: แสดงรายการหนังสือทั้งหมด ---
    render_all_books_list()
    st.divider()

    # --- ส่วนที่ 3: ลบและแก้ไขข้อมูลหนังสือ ---
    render_manage_books_section()

def render_add_book_section():
    st.subheader("เพิ่มข้อมูลหนังสือใหม่")
    st.text_input("ชื่อหนังสือ", key="new_title")
    st.text_input("ผู้แต่ง", key="new_author")

    col1, col2 = st.columns([1, 3])
    with col1:
        st.button("บันทึกข้อมูลหนังสือ", on_click=save_book_controller)
    with col2:
        st.button("ล้างฟอร์ม", on_click=reset_book_form)

def render_all_books_list():
    st.subheader("📖 รายการหนังสือทั้งหมดในระบบ")
    books_df = get_all_books()
    if books_df.empty:
        st.info("ยังไม่มีข้อมูลหนังสือในระบบ")
    else:
        st.dataframe(books_df, use_container_width=True)

def render_manage_books_section():
    books_df = get_all_books()

    st.subheader("🗑 ลบข้อมูลหนังสือ")
    if books_df.empty:
        st.info("ยังไม่มีข้อมูลหนังสือในระบบ")
    else:
        for _, row in books_df.iterrows():
            col1, col2, col3 = st.columns([4, 3, 1])
            with col1:
                st.write(f"📘 **{row['title']}** — {row['author']}")
            with col2:
                st.write(f"รหัสหนังสือ: {row['id']}")
            with col3:
                if st.button("ลบ", key=f"delete_book_{row['id']}"):
                    delete_book_controller(row["id"])

    st.subheader("✏️ แก้ไขข้อมูลหนังสือ")
    if books_df.empty:
        st.info("ยังไม่มีข้อมูลให้แก้ไข")
    else:
        search_title = st.text_input("ค้นหาชื่อหนังสือที่ต้องการแก้ไข")
        if search_title.strip():
            filtered_df = books_df[books_df["title"].str.contains(search_title.strip(), case=False)]
        else:
            filtered_df = books_df

        if filtered_df.empty:
            st.warning("ไม่พบหนังสือตามคำค้นหา")
        else:
            book_options = [f"{row['id']} - {row['title']}" for _, row in filtered_df.iterrows()]
            selected_book = st.selectbox("เลือกหนังสือที่จะแก้ไข", book_options)
            book_id = int(selected_book.split(" - ")[0])
            selected_row = books_df[books_df["id"] == book_id].iloc[0]

            with st.form("edit_book_form"):
                new_title = st.text_input("ชื่อหนังสือ", value=selected_row["title"])
                new_author = st.text_input("ผู้แต่ง", value=selected_row["author"])
                save_update = st.form_submit_button("บันทึกการแก้ไข")

            if save_update:
                update_book_controller(book_id, new_title, new_author)