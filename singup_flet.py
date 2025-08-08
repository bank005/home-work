import flet as ft
import csv, os, re
from datetime import datetime

# หา path ของโฟลเดอร์ที่ไฟล์ .py นี้อยู่
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "regis.csv")

DIGITS = re.compile(r"\d")

def ensure_csv():
    """สร้างไฟล์ CSV พร้อมหัวตารางถ้ายังไม่มี"""
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["วันที่-เวลา", "ชื่อ-สกุล", "โทรศัพท์", "ชื่อทีม"])

def main(page: ft.Page):
    page.title = "แบบฟอร์มรับสมัคร → CSV"
    page.window_min_width = 420
    page.window_min_height = 520

    ensure_csv()

    name = ft.TextField(label="ชื่อ-สกุล", autofocus=True, expand=True)
    phone = ft.TextField(
        label="หมายเลขโทรศัพท์",
        hint_text="เช่น 0812345678",
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9+ ]"),
        expand=True,
    )
    team = ft.TextField(label="ชื่อทีม", expand=True)
    msg = ft.Text(value="", selectable=True)

    def show_ok(text: str):
        page.snack_bar = ft.SnackBar(ft.Text(text), open=True)
        page.update()

    def show_err(text: str):
        page.snack_bar = ft.SnackBar(ft.Text(text), open=True, bgcolor="#ffdbdb")
        page.update()

    def clear_fields(_=None):
        name.value = phone.value = team.value = ""
        msg.value = ""
        page.update()

    def on_save(_):
        n = (name.value or "").strip()
        p = (phone.value or "").strip()
        t = (team.value or "").strip()

        errs = []
        if not n: errs.append("กรุณากรอก ชื่อ-สกุล")
        if not p: errs.append("กรุณากรอก หมายเลขโทรศัพท์")
        if not t: errs.append("กรุณากรอก ชื่อทีม")
        if p and len(DIGITS.findall(p)) < 9:
            errs.append("หมายเลขโทรศัพท์สั้นเกินไป (อย่างน้อย 9 หลัก)")

        if errs:
            show_err(" • " + " | ".join(errs))
            return

        ensure_csv()
        with open(CSV_PATH, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), n, p, t])

        show_ok("บันทึกเรียบร้อย ✅ (regis.csv)")
        msg.value = f"บันทึกไปที่: {CSV_PATH}"
        clear_fields()

    save_btn = ft.ElevatedButton("บันทึก", on_click=on_save)
    clear_btn = ft.OutlinedButton("ล้าง", on_click=clear_fields)

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("แบบฟอร์มการรับสมัคร", size=22, weight="bold"),
                    name, phone, team,
                    ft.Row([save_btn, clear_btn], spacing=12),
                    msg,
                    ft.Text(f"**ไฟล์จะถูกบันทึกในโฟลเดอร์เดียวกับไฟล์โปรแกรมนี้**", size=12),
                ],
                spacing=12,
                tight=True,
            ),
            padding=20,
            width=520,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
