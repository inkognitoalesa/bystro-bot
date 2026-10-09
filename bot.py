import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🚴 Курьер / Доставка", callback_data="cat_courier")],
        [InlineKeyboardButton(text="📦 Склад / Сборка / Комплектовка", callback_data="cat_warehouse")],
        [InlineKeyboardButton(text="❓ Частые вопросы (FAQ)", callback_data="faq")],
        [InlineKeyboardButton(text="💬 Связь с куратором", callback_data="support")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_courier_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🟢 Яндекс Еда (Пеший / Вело / Авто)", url="https://pampadu.ru/")],
        [InlineKeyboardButton(text="🟡 СберМаркет / Купер", url="https://pampadu.ru/")],
        [InlineKeyboardButton(text="🔵 Ozon fresh курьер", url="https://pampadu.ru/")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_warehouse_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📦 Склад Ozon (Сборка / Комплектовка)", url="https://pampadu.ru/")],
        [InlineKeyboardButton(text="🏬 Склад Wildberries", url="https://pampadu.ru/")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]]
    )

@dp.message(CommandStart())
async def handle_start(message: Message):
    welcome_text = (
        "👋 **Добро пожаловать в сервис подбора смен «Быстро Смена»!**\n\n"
        "Мы помогаем быстро найти проверенную подработку и смены рядом с домом:\n"
        "• Ежедневные / еженедельные выплаты\n"
        "• Свободный график и выбор локации\n"
        "• Бесплатное оформление и поддержка куратора\n\n"
        "Выберите интересующее направление ниже 👇"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@dp.callback_query(F.data == "cat_courier")
async def show_courier_vacancies(callback: CallbackQuery):
    await callback.message.edit_text(
        "🚴 **Направление: Курьер и Доставка**\n\n"
        "• Доход: до 5 000 — 9 000 ₽ за смену\n"
        "• Выплаты: ежедневно или еженедельно\n"
        "• Можно пешком, на велосипеде, самокате или авто\n\n"
        "Выберите партнёра для оформления заявки:",
        reply_markup=get_courier_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "cat_warehouse")
async def show_warehouse_vacancies(callback: CallbackQuery):
    await callback.message.edit_text(
        "📦 **Направление: Склад и Логистика**\n\n"
        "• Доход: от 3 500 до 7 000 ₽ за смену\n"
        "• Обязанности: комплектация, сборка, сортировка товаров\n"
        "• Предоставляется форма и корпоративный транспорт\n\n"
        "Выберите склад для оформления заявки:",
        reply_markup=get_warehouse_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery):
    faq_text = (
        "❓ **Часто задаваемые вопросы:**\n\n"
        "1. **Берут ли без опыта?**\n"
        "— Да, стажировка проходит на месте в первый рабочий день.\n\n"
        "2. **Когда приходят первые деньги?**\n"
        "— Зависит от партнера: у большинства вывод доступен сразу после смены на карту.\n\n"
        "3. **Сколько часов длится смена?**\n"
        "— От 4 до 12 часов по вашему выбору."
    )
    await callback.message.edit_text(faq_text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "support")
async def show_support(callback: CallbackQuery):
    support_text = (
        "💬 **Поддержка куратора**\n\n"
        "Если у вас есть вопросы по оформлению, документам или смене:\n"
        "Напишите куратору: @inkognitoalesa"
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
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
