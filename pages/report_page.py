import streamlit as st
import model
from datetime import date
import io
import pandas as pd
import plotly.express as px

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def render_report():
    st.subheader("📊 รายงานสรุประบบยืม-คืนหนังสือ")

    # =========================
    # 1) กราฟวงกลม : สถานะหนังสือ
    # =========================
    st.markdown("### 1) สัดส่วนหนังสือตามสถานะ")

    status_df = model.get_book_status_summary()

    if status_df.empty:
        st.info("ไม่มีข้อมูลหนังสือ")
    else:
        fig = px.pie(
            status_df,
            names="สถานะหนังสือ",
            values="จำนวน",
            hole=0.4,
            title="สัดส่วนหนังสือตามสถานะ"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(status_df, use_container_width=True)

    st.divider()

    # =========================
    # 2) กราฟแท่ง : จำนวนการยืมรายเดือน
    # =========================
    st.markdown("### 2) จำนวนการยืมรายเดือน")

    col1, col2 = st.columns(2)

    with col1:
        month_start = st.date_input(
            "วันที่เริ่มต้น (กราฟรายเดือน)",
            value=date(2025, 6, 1)
        )

    with col2:
        month_end = st.date_input(
            "วันที่สิ้นสุด (กราฟรายเดือน)",
            value=date.today()
        )

    if month_start > month_end:
        st.warning("วันที่เริ่มต้นต้องไม่มากกว่าวันที่สิ้นสุด")
        return

    monthly_df = model.get_borrow_summary_by_month(
        month_start.isoformat(),
        month_end.isoformat()
    )

    if monthly_df.empty:
        st.info("ไม่พบข้อมูลการยืมในช่วงเวลาที่เลือก")
    else:
        st.bar_chart(monthly_df.set_index("เดือน")["จำนวนการยืม"])
        st.dataframe(monthly_df, use_container_width=True)

    st.divider()

    # ===============================
    # 3) รายการผู้ยืม–คืนทั้งหมด
    # ===============================
    st.markdown("### 3) รายการผู้ยืม–คืนทั้งหมด")

    col1, col2, col3 = st.columns(3)

    with col1:
        report_start = st.date_input(
            "วันที่เริ่มต้น (รายงาน)",
            value=date(2025, 6, 1)
        )

    with col2:
        report_end = st.date_input(
            "วันที่สิ้นสุด (รายงาน)",
            value=date.today()
        )

    with col3:
        status_label = st.selectbox(
            "สถานะการยืม–คืน",
            ["ทั้งหมด", "ยังไม่คืน", "คืนแล้ว"]
        )

    if report_start > report_end:
        st.warning("วันที่เริ่มต้นต้องไม่มากกว่าวันที่สิ้นสุด")
        return

    status_map = {
        "ทั้งหมด": "all",
        "ยังไม่คืน": "borrowed",
        "คืนแล้ว": "returned"
    }

    report_df = model.get_borrow_report(
        report_start.isoformat(),
        report_end.isoformat(),
        status_map[status_label]
    )

    if report_df.empty:
        st.info("ไม่พบข้อมูลตามเงื่อนไขที่เลือก")
        return

    st.dataframe(report_df, use_container_width=True)

    # ===============================
    # 4) ส่งออกรายงาน
    # ===============================
    st.markdown("### 4) ส่งออกรายงาน")

    # ---------- CSV ----------
    csv_buffer = io.StringIO()
    report_df.to_csv(csv_buffer, index=False)

    st.download_button(
        label="⬇️ ดาวน์โหลดรายงาน (CSV)",
        data=csv_buffer.getvalue(),
        file_name="borrow_return_report.csv",
        mime="text/csv"
    )

    # ---------- Excel ----------
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer) as writer:
        report_df.to_excel(writer, index=False, sheet_name="BorrowReport")

    st.download_button(
        label="⬇️ ดาวน์โหลดรายงาน (Excel)",
        data=excel_buffer.getvalue(),
        file_name="borrow_return_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # ---------- PDF (ภาษาไทย / ฟอนต์เดียว) ----------
    pdf_buffer = io.BytesIO()

    # register ฟอนต์ไทย (ไฟล์เดียว)
    pdfmetrics.registerFont(
        TTFont("THSarabun", "fonts/THSarabunNew.ttf")
    )

    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4

    # Title (ขนาดใหญ่แทน Bold)
    c.setFont("THSarabun", 20)
    c.drawCentredString(
        width / 2,
        height - 2 * cm,
        "รายงานผู้ยืม–คืนหนังสือ"
    )

    # Meta
    c.setFont("THSarabun", 14)
    c.drawString(
        2 * cm,
        height - 3 * cm,
        f"ช่วงวันที่: {report_start} ถึง {report_end} | สถานะ: {status_label}"
    )

    y = height - 4 * cm

    # คำนวณคอลัมน์อัตโนมัติ
    num_cols = len(report_df.columns)
    usable_width = width - 4 * cm
    col_width = usable_width / num_cols

    # Header
    c.setFont("THSarabun", 15)
    for i, col in enumerate(report_df.columns):
        c.drawString(2 * cm + i * col_width, y, str(col))

    y -= 0.8 * cm

    # Rows
    c.setFont("THSarabun", 14)
    for _, row in report_df.iterrows():
        for i, value in enumerate(row):
            c.drawString(2 * cm + i * col_width, y, str(value))

        y -= 0.7 * cm

        if y < 2 * cm:
            c.showPage()
            c.setFont("THSarabun", 14)
            y = height - 2 * cm

    c.save()
    pdf_buffer.seek(0)

    st.download_button(
        label="⬇️ ดาวน์โหลดรายงาน (PDF)",
        data=pdf_buffer,
        file_name="borrow_return_report.pdf",
        mime="application/pdf"
    )
