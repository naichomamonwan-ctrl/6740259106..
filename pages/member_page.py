import streamlit as st
from model import get_all_members
from controller import (
    reset_member_form,
    validate_and_save_member_controller,
    delete_member_controller,
    validate_and_update_member_controller
)

def render_member_page():
    """ฟังก์ชันหลักสำหรับหน้าจัดการสมาชิก"""
    st.header("👤 จัดการข้อมูลสมาชิก")

    # --- ส่วนที่ 1: สมัครสมาชิกใหม่ ---
    render_add_member_section()
    st.divider()

    # --- ส่วนที่ 2: จัดการสมาชิกเดิม: ลบ + แก้ไข ---
    render_manage_members_section()

def render_add_member_section():
    st.subheader("สมัครสมาชิกใหม่")
    with st.form("member_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            member_code = st.text_input("รหัสสมาชิก (เช่น M001)", max_chars=10, key="member_code")
            member_name = st.text_input("ชื่อ - สกุล", key="member_name")
            gender = st.selectbox("เพศ", ["ไม่ระบุ", "หญิง", "ชาย", "อื่น ๆ"], key="gender")
        with col_b:
            email = st.text_input("อีเมล", key="member_email")
            phone = st.text_input("เบอร์โทรศัพท์", key="member_phone")
            is_active = st.checkbox("ยังใช้งานอยู่", value=True, key="is_active")

        btn_col1, btn_col2 = st.columns([1, 3])
        with btn_col1:
            submitted = st.form_submit_button("บันทึกข้อมูลสมาชิก")
        with btn_col2:
            st.form_submit_button("ล้างฟอร์ม", on_click=reset_member_form)

    if submitted:
        validate_and_save_member_controller(member_code, member_name, gender, email, phone, is_active)

def render_manage_members_section():
    members_df = get_all_members()

    st.subheader("📋 รายชื่อสมาชิกทั้งหมด")
    if members_df.empty:
        st.info("ยังไม่มีข้อมูลสมาชิกในระบบ")
    else:
        for _, row in members_df.iterrows():
            col1, col2, col3, col4 = st.columns([3, 3, 2, 1])
            with col1:
                st.write(f"**{row['รหัสสมาชิก']}** : {row['ชื่อสกุล']}")
            with col2:
                st.write(row["อีเมล"] if row["อีเมล"] else "-")
            with col3:
                st.write(row["สถานะ"])
            with col4:
                if st.button("ลบ", key=f"delete_member_{row['id']}"):
                    delete_member_controller(row["id"], row["ชื่อสกุล"])

    st.subheader("✏️ แก้ไขข้อมูลสมาชิก")
    if members_df.empty:
        st.info("ยังไม่มีข้อมูลให้แก้ไข")
    else:
        member_options = [f"{row['id']} - {row['รหัสสมาชิก']} : {row['ชื่อสกุล']}" for _, row in members_df.iterrows()]
        selected = st.selectbox("เลือกสมาชิกที่จะแก้ไข", member_options)
        selected_id = int(selected.split(" - ")[0])
        selected_row = members_df[members_df["id"] == selected_id].iloc[0]

        with st.form("edit_member_form"):
            col1, col2 = st.columns(2)
            with col1:
                edit_member_code = st.text_input("รหัสสมาชิก", value=selected_row["รหัสสมาชิก"])
                edit_name = st.text_input("ชื่อ - สกุล", value=selected_row["ชื่อสกุล"])
                edit_gender = st.selectbox("เพศ", ["ไม่ระบุ", "หญิง", "ชาย", "อื่น ๆ"], 
                                         index=["ไม่ระบุ", "หญิง", "ชาย", "อื่น ๆ"].index(selected_row["เพศ"] if selected_row["เพศ"] else "ไม่ระบุ"))
            with col2:
                edit_email = st.text_input("อีเมล", value=selected_row["อีเมล"] if selected_row["อีเมล"] else "")
                edit_phone = st.text_input("เบอร์โทรศัพท์", value=selected_row["เบอร์โทร"] if selected_row["เบอร์โทร"] else "")
                edit_is_active = st.checkbox("ยังใช้งานอยู่", value=(selected_row["สถานะ"] == "ใช้งาน"))

            update_submitted = st.form_submit_button("บันทึกการแก้ไข")

        if update_submitted:
            validate_and_update_member_controller(selected_id, edit_member_code, edit_name, edit_gender, edit_email, edit_phone, edit_is_active, selected_row)