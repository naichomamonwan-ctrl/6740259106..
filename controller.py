# controller.py

import streamlit as st
import re
import pandas as pd
import hashlib
import model  # นำเข้า model เพื่อใช้เรียก model.function_name()

# ---------------- ฟังก์ชัน Utility ภายใน Controller ----------------

def _hash_password(pw: str) -> str:
    """เข้ารหัสผ่านด้วย SHA-256"""
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

# ---------------- ฟังก์ชัน Controller สำหรับหนังสือ ----------------

def reset_book_form():
    """ล้างค่าช่องกรอกชื่อหนังสือและผู้แต่ง (View Utility)"""
    st.session_state["new_title"] = ""
    st.session_state["new_author"] = ""

def save_book_controller():
    """อ่านค่าจาก View → ตรวจสอบ → บันทึกลงฐาน (Model) → รีเซ็ตฟอร์ม"""
    title = st.session_state.get("new_title", "").strip()
    author = st.session_state.get("new_author", "").strip()

    if title == "":
        st.error("⚠ กรุณากรอกชื่อหนังสือ")
    else:
        model.add_book_db(title, author)
        st.success(f"✅ บันทึก '{title}' สำเร็จแล้ว")
        reset_book_form()

def delete_book_controller(book_id: int):
    """เรียก Model เพื่อลบหนังสือและแสดงผล"""
    model.delete_book_db(book_id)
    st.success("ลบข้อมูลหนังสือเรียบร้อยแล้ว")
    st.rerun()

def update_book_controller(book_id: int, new_title: str, new_author: str):
    """ตรวจสอบ input และเรียก Model เพื่ออัปเดตหนังสือ"""
    if new_title.strip() == "":
        st.error("กรุณากรอกชื่อหนังสือ")
    else:
        model.update_book_db(book_id, new_title.strip(), new_author.strip())
        st.success("แก้ไขข้อมูลหนังสือเรียบร้อยแล้ว")
        st.rerun()

# ---------------- ฟังก์ชัน Controller สำหรับสมาชิก ----------------

def reset_member_form():
    """ล้างค่าฟิลด์ทั้งหมดในฟอร์มสมัครสมาชิก (View Utility)"""
    st.session_state["member_code"] = ""
    st.session_state["member_name"] = ""
    st.session_state["gender"] = "ไม่ระบุ"
    st.session_state["member_email"] = ""
    st.session_state["member_phone"] = ""
    st.session_state["is_active"] = True

def validate_and_save_member_controller(member_code, name, gender, email, phone, is_active):
    """ตรวจสอบความถูกต้องของข้อมูลสมาชิกก่อนบันทึก (CREATE)"""
    errors = []
    member_code = member_code.strip()
    name = name.strip()
    email = email.strip()
    phone = phone.strip()

    if member_code == "":
        errors.append("กรุณากรอก **รหัสสมาชิก**")
    if name == "":
        errors.append("กรุณากรอก **ชื่อ - สกุล**")

    if email:
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_pattern, email):
            errors.append("รูปแบบ **อีเมลไม่ถูกต้อง**")

    if member_code and model.is_member_code_exists(member_code):
        errors.append(f"รหัสสมาชิก **{member_code}** มีอยู่แล้วในระบบ")
    
    if email and model.is_email_exists(email):
        errors.append(f"อีเมล **{email}** ถูกใช้สมัครแล้ว")

    if errors:
        for err in errors:
            st.error("⚠ " + err)
        return False
    else:
        model.add_member_db(member_code, name, gender, email, phone, is_active)
        st.success(f"✅ บันทึกข้อมูลสมาชิก '{name}' สำเร็จแล้ว")
        return True

def delete_member_controller(member_id: int, member_name: str):
    """เรียก Model เพื่อลบสมาชิก"""
    model.delete_member_db(member_id)
    st.success(f"ลบสมาชิก {member_name} เรียบร้อยแล้ว")
    st.rerun()

def validate_and_update_member_controller(selected_id, edit_member_code, edit_name, edit_gender, edit_email, edit_phone, edit_is_active, selected_row):
    """ตรวจสอบความถูกต้องของข้อมูลสมาชิกก่อนอัปเดต (UPDATE)"""
    errors = []
    edit_member_code = edit_member_code.strip()
    edit_name = edit_name.strip()
    edit_email = edit_email.strip()

    if edit_member_code == "":
        errors.append("กรุณากรอก **รหัสสมาชิก**")
    if edit_name == "":
        errors.append("กรุณากรอก **ชื่อ - สกุล**")

    if edit_email:
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_pattern, edit_email):
            errors.append("รูปแบบ **อีเมลไม่ถูกต้อง**")

    old_code = selected_row["รหัสสมาชิก"]
    if edit_member_code and edit_member_code != old_code and model.is_member_code_exists(edit_member_code):
        errors.append(f"รหัสสมาชิก **{edit_member_code}** มีอยู่แล้วในระบบ")

    old_email = selected_row["อีเมล"] or ""
    if edit_email and edit_email != old_email and model.is_email_exists(edit_email):
        errors.append(f"อีเมล **{edit_email}** ถูกใช้สมัครแล้ว")

    if errors:
        for err in errors:
            st.error("⚠ " + err)
        return False
    else:
        model.update_member_db(selected_id, edit_member_code, edit_name, edit_gender, edit_email, edit_phone, edit_is_active)
        st.success("✅ แก้ไขข้อมูลสมาชิกเรียบร้อยแล้ว")
        st.rerun()
        return True

# ---------------- ฟังก์ชัน Controller สำหรับ User & Login ----------------

def login(username: str, password: str):
    """Login (มีการเช็คสถานะการใช้งาน)"""
    errors = []
    if not username.strip():
        errors.append("กรุณากรอก **ชื่อผู้ใช้**")
    if not password.strip():
        errors.append("กรุณากรอก **รหัสผ่าน**")
        
    if errors:
        return False, errors, None
        
    u = model.get_user_auth_row(username)
    if not u:
        return False, ["⚠️ ไม่พบบัญชีผู้ใช้นี้ในระบบ"], None
        
    if u.get("is_active") != 1:
        return False, ["⚠️ บัญชีนี้ถูกปิดใช้งาน กรุณาติดต่อผู้ดูแลระบบ"], None
        
    if _hash_password(password) != u["password_hash"]:
        return False, ["⚠️ รหัสผ่านไม่ถูกต้อง"], None
        
    user_info = {"id": u["id"], "username": u["username"], "role": u["role"]}
    return True, ["✅ เข้าสู่ระบบสำเร็จ"], user_info

# -------- Admin actions --------

def create_user(username: str, password: str, role: str, is_active: bool = True):
    """สร้างผู้ใช้ใหม่โดย Admin"""
    errors = []
    username_clean = username.strip()
    
    if not username_clean:
        errors.append("กรุณากรอก **ชื่อผู้ใช้**")
    elif len(username_clean) < 3:
        errors.append("ชื่อผู้ใช้ต้องมีอย่างน้อย 3 ตัวอักษร")
        
    if not password.strip():
        errors.append("กรุณากรอก **รหัสผ่าน**")
    elif len(password.strip()) < 4:
        errors.append("รหัสผ่านต้องมีอย่างน้อย 4 ตัวอักษร")
        
    if role not in ("admin", "staff"):
        errors.append("role ต้องเป็น admin หรือ staff")
        
    if username_clean and model.is_username_exists(username_clean):
        errors.append(f"ชื่อผู้ใช้ **{username_clean}** มีอยู่แล้ว")

    if errors:
        return False, errors

    model.add_user(
        username=username_clean,
        password_hash=_hash_password(password),
        role=role,
        is_active=1 if is_active else 0
    )
    return True, [f"✔️ เพิ่มผู้ใช้ '{username_clean}' เรียบร้อยแล้ว"]

def set_user_role(user_id: int, new_role: str, current_username: str):
    """เปลี่ยนสิทธิ์ผู้ใช้ (ป้องกันการลดสิทธิ์ตัวเอง)"""
    if new_role not in ("admin", "staff"):
        return False, ["role ต้องเป็น admin หรือ staff"]
        
    users_df = model.get_all_users()
    me = users_df[users_df["username"] == current_username]
    
    if not me.empty and int(me.iloc[0]["id"]) == int(user_id) and new_role != "admin":
        return False, ["ไม่อนุญาตให้ลดสิทธิ์ของผู้ดูแลระบบที่กำลังล็อกอินอยู่"]
        
    model.update_user_role(int(user_id), new_role)
    return True, ["✔️ เปลี่ยน role เรียบร้อยแล้ว"]

def set_user_active(user_id: int, is_active: bool, current_username: str):
    """เปิด/ปิด การใช้งานบัญชี (ป้องกันการปิดบัญชีตัวเอง)"""
    users_df = model.get_all_users()
    me = users_df[users_df["username"] == current_username]
    
    if not me.empty and int(me.iloc[0]["id"]) == int(user_id) and (not is_active):
        return False, ["ไม่อนุญาตให้ปิดใช้งานบัญชีที่กำลังล็อกอินอยู่"]
        
    model.update_user_active(int(user_id), 1 if is_active else 0)
    return True, ["✔️ เปลี่ยนสถานะผู้ใช้เรียบร้อยแล้ว"]
    

    ################################
    #################################################
# user login
#################################################
# --- เพิ่มท้ายไฟล์ controller.py ---

import hashlib


# ---------- Utils ----------
def _hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()


# ---------- Controller ----------
def login(username: str, password: str):
    """
    Controller-level login
    return: (ok: bool, messages: list[str], user_info: dict | None)
    user_info: {"id": .., "username": .., "role": ..}
    """
    errors = []

    if not username.strip():
        errors.append("กรุณากรอก **ชื่อผู้ใช้**")
    if not password.strip():
        errors.append("กรุณากรอก **รหัสผ่าน**")

    if errors:
        return False, errors, None

    u = model.get_user_auth_row(username)

    if not u:
        return False, ["⚠ ไม่พบบัญชีผู้ใช้นี้ในระบบ"], None

    if _hash_password(password) != u["password_hash"]:
        return False, ["⚠ รหัสผ่านไม่ถูกต้อง"], None

    user_info = {
        "id": u["id"],
        "username": u["username"],
        "role": u["role"]
    }

    return True, ["✅ เข้าสู่ระบบสำเร็จ"], user_info

# ============================================================
# Borrow: multi-book per transaction
# ============================================================
def borrow_books(member_id: int, staff_user_id: int, due_date_iso: str | None, book_ids: list[int], note: str | None = None):
    """
    สร้างรายการยืม 1 ครั้ง (หลายเล่ม)
    - ต้องระบุ staff_user_id เพื่อบันทึกว่าใครเป็นผู้ทำรายการ
    """
    errors = []
    if not member_id:
        errors.append("กรุณาเลือกสมาชิก")
    if not staff_user_id:
        errors.append("ไม่พบข้อมูลผู้ทำรายการ (กรุณาเข้าสู่ระบบใหม่)")
    if not book_ids:
        errors.append("กรุณาเลือกหนังสืออย่างน้อย 1 เล่ม")
    if errors:
        return False, errors, None


    try:
        tx_id = model.create_borrow_transaction(
            member_id=int(member_id),
            staff_user_id=int(staff_user_id),
            default_due_date=due_date_iso,
            book_ids=[int(x) for x in book_ids],
            note=note
        )
        return True, [f"บันทึกการยืมเรียบร้อยแล้ว (TX: {tx_id})"], tx_id
    except Exception as e:
        return False, [f"ไม่สามารถบันทึกการยืมได้: {e}"], None


def return_book_item(item_id: int, return_staff_user_id: int):
    """คืนหนังสือทีละเล่ม พร้อมบันทึกผู้ทำรายการคืน"""
    if not item_id:
        return False, ["กรุณาเลือกรายการที่จะคืน"]
    if not return_staff_user_id:
        return False, ["ไม่พบข้อมูลผู้ทำรายการ (กรุณาเข้าสู่ระบบใหม่)"]


    ok = model.return_borrow_item(int(item_id), int(return_staff_user_id))
    if not ok:
        return False, ["ไม่พบรายการที่ยังไม่คืน หรือรายการถูกคืนแล้ว"]
    return True, ["บันทึกการคืนเรียบร้อยแล้ว"]


def return_book_items(item_ids: list[int], return_staff_user_id: int):
    """
    คืนหนังสือหลายรายการ (ติ๊กได้หลายเล่ม) พร้อมบันทึกผู้ทำรายการคืน
    return: (ok:bool, messages:list[str])
    """
    if not item_ids:
        return False, ["กรุณาเลือกรายการที่จะคืนอย่างน้อย 1 รายการ"]
    if not return_staff_user_id:
        return False, ["ไม่พบข้อมูลผู้ทำรายการ (กรุณาเข้าสู่ระบบใหม่)"]


    success = 0
    failed = []


    for item_id in item_ids:
        try:
            ok = model.return_borrow_item(int(item_id), int(return_staff_user_id))
            if ok:
                success += 1
            else:
                failed.append(int(item_id))
        except Exception:
            failed.append(int(item_id))


    msgs = [f"บันทึกการคืนสำเร็จ {success} รายการ"]
    if failed:
        msgs.append(f"รายการที่คืนไม่สำเร็จ/ถูกคืนแล้ว: {failed}")


    return True, msgs

