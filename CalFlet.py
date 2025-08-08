# file: CalFlet.py
import re
import flet as ft

ALLOWED = re.compile(r"^[1-9+\-*/\s]+$")

def main(page: ft.Page):
    page.title = "Flet Calculator (1-9, + - * /)"
    page.window_min_width = 320
    page.window_min_height = 420
    page.theme_mode = ft.ThemeMode.LIGHT

    display = ft.TextField(
        value="",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        border_radius=12,
        height=60,
        text_size=24,
        content_padding=ft.padding.symmetric(10, 12),
        expand=True,
    )

    def mk_btn(label, on_click=None):
        return ft.ElevatedButton(
            label,
            on_click=on_click or on_btn_click,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
            expand=1,
        )

    def on_btn_click(e: ft.ControlEvent):
        t = e.control.text
        if t == "C":
            display.value = ""
        elif t == "=":
            expr = display.value.strip()
            if not expr:
                return
            if not ALLOWED.match(expr):
                display.value = "ERROR"
            else:
                try:
                    display.value = str(eval(expr))
                except Exception:
                    display.value = "ERROR"
        else:
            display.value += f" {t} " if t in {"+", "-", "*", "/"} else t
        page.update()

    rows = [
        ["1", "2", "3", "+"],
        ["4", "5", "6", "-"],
        ["7", "8", "9", "*"],
        ["C", "=", "/"],
    ]

    grid = [ft.Row([mk_btn(x) for x in row], spacing=10, expand=True) for row in rows]

    page.add(ft.Container(padding=20, content=ft.Column(
        controls=[display, ft.Container(height=12), *grid],
        spacing=12
    )))

if __name__ == "__main__":
    ft.app(main)
