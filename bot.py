import os
import sqlite3
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Вставьте сюда ваш числовой Telegram ID (узнать можно в @userinfobot)
ADMIN_ID = 8291221045

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- БАЗА ДАННЫХ ДЛЯ АНАЛИТИКИ (SQLite) ---
DB_NAME = "stats.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_user(user_id: int, username: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username or ""))
    conn.commit()
    conn.close()

def log_click(user_id: int, category: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO clicks (user_id, category) VALUES (?, ?)", (user_id, category))
    conn.commit()
    conn.close()

def get_analytics():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT category, COUNT(*) FROM clicks GROUP BY category")
    clicks_data = dict(cur.fetchall())
    conn.close()
    return total_users, clicks_data

# Партнерские ссылки Pampadu
COURIER_LINK = "https://trk.ppdu.ru/click/lRpy1nrx?erid=CQH36pWzJqVGXC5oLP8WVVNCNqJmbhiUPijGiu4zpwPd7G"
TRUCK_LINK = "https://trk.ppdu.ru/click/AZv8hynP?erid=CQH36pWzJqVGXC5oTTDpMBk8ei82kpZxV9ZJ1ZC292TAKx"
LAVKA_LINK = "https://trk.ppdu.ru/click/1F5Kat49?erid=CQH36pWzJqVGXC5oUHvq1FTH2g3oi1KL72bsqkyo9iVXM7"

# Главное меню
def get_main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🚴 Курьер (Пеший / Вело / Авто)", callback_data="cat_courier")],
        [InlineKeyboardButton(text="🚛 Грузовой курьер / Водитель с авто", callback_data="cat_truck")],
        [InlineKeyboardButton(text="📦 Склад / Сборка / Комплектовка (Лавка)", callback_data="cat_warehouse")],
        [InlineKeyboardButton(text="❓ Частые вопросы (FAQ)", callback_data="faq")],
        [InlineKeyboardButton(text="💬 Связь с куратором", callback_data="support")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатуры направлений (кнопка перехода сначала фиксирует клик)
def get_courier_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🟢 Оформить анкету курьера", callback_data="apply_courier")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_truck_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🚛 Подать заявку (Водитель на авто)", callback_data="apply_truck")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_warehouse_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📦 Подать заявку (Яндекс Лавка)", callback_data="apply_warehouse")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]]
    )

@dp.message(CommandStart())
async def handle_start(message: Message):
    log_user(message.from_user.id, message.from_user.username)
    welcome_text = (
        "👋 **Добро пожаловать в сервис подбора смен «Быстро Смена»!**\n\n"
        "Мы помогаем быстро найти проверенную подработку и смены рядом с домом:\n"
        "• Ежедневные / еженедельные выплаты\n"
        "• Свободный график и выбор локации\n"
        "• Быстрое онлайн-оформление и поддержка куратора\n\n"
        "Выберите интересующее направление ниже 👇"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

# Команда статистики для администратора
@dp.message(Command("stats"))
async def handle_stats(message: Message):
    if ADMIN_ID != 0 and message.from_user.id != ADMIN_ID:
        return

    total_users, clicks = get_analytics()
    courier_clicks = clicks.get("Курьер", 0)
    truck_clicks = clicks.get("Грузовой", 0)
    warehouse_clicks = clicks.get("Склад (Лавка)", 0)
    support_clicks = clicks.get("Куратор", 0)
    total_clicks = courier_clicks + truck_clicks + warehouse_clicks

    stats_msg = (
        "📊 **Аналитика сервиса «Быстро Смена»**\n\n"
        f"👥 **Всего пользователей:** {total_users}\n"
        f"🎯 **Всего переходов к заявкам:** {total_clicks}\n\n"
        "**Переходы по направлениям:**\n"
        f"• 🚴 Курьер: {courier_clicks}\n"
        f"• 🚛 Грузовой/водитель: {truck_clicks}\n"
        f"• 📦 Склад (Лавка): {warehouse_clicks}\n\n"
        f"💬 **Кликов «Связь с куратором»:** {support_clicks}"
    )
    await message.answer(stats_msg, parse_mode="Markdown")

@dp.callback_query(F.data == "cat_courier")
async def show_courier_vacancies(callback: CallbackQuery):
    await callback.message.edit_text(
        "🚴 **Направление: Курьерская доставка**\n\n"
        "• **Формат:** пешком, на велосипеде, самокате или личном авто\n"
        "• **Доход:** до 9 000 ₽ за смену (в зависимости от выбранного региона)\n"
        "• **Выплаты:** ежедневно или еженедельно на карту\n"
        "• **График:** полностью свободный (смены от 2-4 часов)\n"
        "• Бесплатная экипировка и термосумка\n\n"
        "Нажмите кнопку ниже для быстрой регистрации 👇",
        reply_markup=get_courier_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "apply_courier")
async def apply_courier(callback: CallbackQuery):
    log_click(callback.from_user.id, "Курьер")
    link_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Открыть анкету курьера", url=COURIER_LINK)],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]
    ])
    await callback.message.edit_text(
        "✅ **Переход к официальной анкете курьера**\n\n"
        "Нажмите на кнопку ниже, чтобы заполнить короткую анкету и забронировать первую смену:",
        reply_markup=link_kb,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "cat_truck")
async def show_truck_vacancies(callback: CallbackQuery):
    await callback.message.edit_text(
        "🚛 **Направление: Грузовой курьер / Водитель**\n\n"
        "• **Формат:** на собственном или арендованном грузовом авто (каблук, фургон, Газель)\n"
        "• **Доход:** до 337 000 ₽ в месяц (в зависимости от выбранного региона)\n"
        "• **Выплаты:** моментальный вывод средств\n"
        "• **График:** свободный режим и гибкое расписание\n\n"
        "Нажмите кнопку ниже для отправки заявки 👇",
        reply_markup=get_truck_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "apply_truck")
async def apply_truck(callback: CallbackQuery):
    log_click(callback.from_user.id, "Грузовой")
    link_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Открыть анкету водителя", url=TRUCK_LINK)],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]
    ])
    await callback.message.edit_text(
        "✅ **Переход к заявке для водителей**\n\n"
        "Нажмите кнопку ниже для перехода к регистрации в сервисе:",
        reply_markup=link_kb,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "cat_warehouse")
async def show_warehouse_vacancies(callback: CallbackQuery):
    await callback.message.edit_text(
        "📦 **Направление: Склад / Комплектация (Яндекс Лавка)**\n\n"
        "• **Формат:** работа в тёплом помещении у дома, без разъездов по улице\n"
        "• **Доход:** до 100 000 — 150 000 ₽ в месяц (в зависимости от выбранного региона)\n"
        "• **Обязанности:** сборка и комплектация заказов\n"
        "• **Бонусы:** удобные графики, корпоративные скидки и бесплатное обучение\n\n"
        "Нажмите кнопку ниже для подачи заявки 👇",
        reply_markup=get_warehouse_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "apply_warehouse")
async def apply_warehouse(callback: CallbackQuery):
    log_click(callback.from_user.id, "Склад (Лавка)")
    link_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Открыть анкету (Яндекс Лавка)", url=LAVKA_LINK)],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]
    ])
    await callback.message.edit_text(
        "✅ **Переход к анкете Яндекс Лавки**\n\n"
        "Нажмите кнопку ниже, чтобы отправить заявку на склад/даркстор:",
        reply_markup=link_kb,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery):
    faq_text = (
        "❓ **Часто задаваемые вопросы (FAQ):**\n\n"
        "1. **Берут ли без опыта?**\n"
        "— Да, стажировка и простое обучение проходят в первый же день онлайн или на месте.\n\n"
        "2. **С какого возраста можно начать?**\n"
        "— Большинство направлений доступно с 18 лет, пешие смены в ряде городов — с 16 лет.\n\n"
        "3. **Можно ли совмещать с учёбой или работой?**\n"
        "— Да, смены от 2-4 часов, график и дни выхода вы выбираете самостоятельно.\n\n"
        "4. **Когда приходят деньги?**\n"
        "— Ежедневные или еженедельные выплаты на любую банковскую карту.\n\n"
        "5. **Выдают ли форму и сумку?**\n"
        "— Да, брендированная экипировка и термокороб предоставляются бесплатно.\n\n"
        "6. **Берут ли граждан СНГ?**\n"
        "— Да, при наличии базового пакета документов для работы (паспорт, регистрация, ИНН/СНИЛС/патент)."
    )
    await callback.message.edit_text(faq_text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "support")
async def show_support(callback: CallbackQuery):
    log_click(callback.from_user.id, "Куратор")
    support_text = (
        "💬 **Поддержка куратора**\n\n"
        "Если у вас есть вопросы по оформлению или выходу на смену:\n"
        "Напишите куратору: @bystrosmena"
    )
    await callback.message.edit_text(support_text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню сервиса **«Быстро Смена»**.\nВыберите направление:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

# Микровеб-сервер для поддержания статуса Live на Render
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    init_db()
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
