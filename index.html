import streamlit as st

# นำเข้าโมดูลจากโฟลเดอร์ pages
from pages import book_page
from pages import member_page
from pages import borrow_page
# ✅ เพิ่มเติม: import หน้า admin
from pages import admin_page

# ✅ เพิ่มเติม: import หน้า login (View)
from pages import login_page

from pages import report_page



# ==========================================
# 1. จัดการ Session State และความปลอดภัย
# ==========================================

# ตรวจสอบและตั้งค่าเริ่มต้นสำหรับการเข้าสู่ระบบ
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

# กำหนดหน้าเริ่มต้นของแอป
if "page" not in st.session_state:
    st.session_state.page = "books"

# ==========================================
# 2. ปรับแต่ง UI ด้วย CSS (ซ่อนเมนูมาตรฐานและตกแต่ง)
# ==========================================

st.markdown("""
<style>
/* ซ่อน Multi-page auto nav ของ Streamlit */
section[data-testid="stSidebarNav"] {display: none !important;}
div[data-testid="stSidebarNav"] {display: none !important;}
nav[data-testid="stSidebarNav"] {display: none !important;}
div[data-testid="stSidebarNavItems"] {display: none !important;}
div[data-testid="stSidebarNavSeparator"] {display: none !important;}

/* Fallback สำหรับกรณีโครงสร้าง DOM เปลี่ยน */
aside ul:has(a[href*="?page="]) {display: none !important;}
aside ul:has(a[href*="/book_page"]) {display: none !important;}
aside ul:has(a[href*="/member_page"]) {display: none !important;}
aside ul:has(a[href*="/borrow_page"]) {display: none !important;}

/* ตกแต่งหัวข้อเมนูใน Sidebar */
.menu-title {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. การแสดงผลหน้าจอหลักและ Login Gate
# ==========================================

st.set_page_config(page_title="ระบบยืม-คืนหนังสือ", page_icon="📚")

# ตรวจสอบว่าล็อกอินหรือยัง ถ้ายังให้หยุดและแสดงหน้า Login
if not st.session_state["is_logged_in"]:
    login_page.render_login()
    st.stop()

# แสดงหัวข้อเว็บ (จะเห็นเฉพาะเมื่อล็อกอินแล้วเท่านั้น)
st.title("📚 ระบบยืม-คืนหนังสือ (Streamlit + SQLite)")
st.write("ตัวอย่าง Web App เชื่อมฐานข้อมูล (ปรับโครงสร้างแบบ MVC เชิงแนวคิด)")

# ==========================================
# 4. ฟังก์ชันและเมนูการใช้งาน (Sidebar)
# ==========================================

# ฟังก์ชันสำหรับสร้างปุ่มเมนูที่ควบคุมด้วย session_state
def nav_button(label, key, icon=""):
    active = (st.session_state.page == key)
    btn = st.sidebar.button(
        f"{icon} {label}",
        use_container_width=True,
        key=f"btn_{key}"
    )
    if btn:
        st.session_state.page = key
        st.rerun()


####   เพิ่มการแสดงชื่อผู้ใช้งาน และปุ่ม logout ###########################################
## ✅ เพิ่มเติม: แสดงผู้ใช้ + ปุ่ม Logout
user = st.session_state.get("user") or {}
st.sidebar.markdown(f"👤 ผู้ใช้: **{user.get('username','-')}**")
st.sidebar.markdown(f"🔑 บทบาท: **{user.get('role','-')}**")

if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state["is_logged_in"] = False
        st.session_state["user"] = None
        st.session_state["page"] = "books"
        st.rerun()
####   จบส่วน การเพิ่มการแสดงชื่อผู้ใช้งาน และปุ่ม logout ###########################################


# แสดงหัวข้อเมนู
st.sidebar.markdown("""
<div class="menu-title">
    เมนู
</div>
""", unsafe_allow_html=True)

# ตรวจสอบสิทธิ์ผู้ใช้งาน (Role-based menu)
# หมายเหตุ: 'user' ต้องได้มาจากกระบวนการ login ก่อนหน้านี้
role = st.session_state["user"].get("role", "admin") if st.session_state["user"] else "admin"

# รายการเมนูสำหรับทั้ง Admin และ Staff
nav_button("หนังสือ", "books", "📚")
nav_button("สมาชิก", "members", "👤")
nav_button("ยืม-คืน", "borrows", "🔄")


# เมนูพิเศษเฉพาะ Admin (ปัจจุบันยังถูกคอมเมนต์ไว้)
if role == "admin":
    nav_button("จัดการผู้ใช้", "admin", "🛠️")
    nav_button("รายงาน", "reports", "📊")
    


# ---------- Routing ----------
# ✅ แก้ไขใหม่: ป้องกัน staff เข้าหน้า admin ด้วยการบังคับ routing
# ✅ แก้ไขใหม่: เอาการบังคับ staff ไปหน้า borrows ออก (เพราะ staff ทําได้ทุกอย่างแล้ว)
# ✅ แก้ไขใหม่: เอาการบังคับ staff ไปหน้า borrows ออก (เพราะ staff ทำได้ทุกอย่างแล้ว)

if st.session_state.page == "books":
    book_page.render_book_page()

elif st.session_state.page == "members":
    member_page.render_member_page()

elif st.session_state.page == "borrows":
    borrow_page.render_borrow()


elif st.session_state.page == "reports":
    if role != "admin":
        st.warning("⚠️ หน้านี้อนุญาตเฉพาะผู้ดูแลระบบ (admin) เท่านั้น")
    else:
        report_page.render_report()

elif st.session_state.page == "admin":
    # ✅ เพิ่มเติม: guard กัน staff เข้าหน้า admin แม้พยายามเปลี่ยน state เอง
    if role != "admin":
        st.warning("⚠️ หน้านี้อนุญาตเฉพาะผู้ดูแลระบบ (admin) เท่านั้น")
    else:
        admin_page.render_admin()

else:
    # fallback
    book_page.render_book()

