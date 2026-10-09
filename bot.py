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

# Клавиатура: Курьер
def get_courier_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🟢 Оформить анкету курьера", url=COURIER_LINK)],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура: Грузовой
def get_truck_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🚛 Подать заявку (Водитель на авто)", url=TRUCK_LINK)],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура: Склад / Лавка
def get_warehouse_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📦 Подать заявку (Яндекс Лавка)", url=LAVKA_LINK)],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Кнопка возврата
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
        "• Быстрое онлайн-оформление и поддержка куратора\n\n"
        "Выберите интересующее направление ниже 👇"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@dp.callback_query(F.data == "cat_courier")
async def show_courier_vacancies(callback: CallbackQuery):
    await callback.message.edit_text(
        "🚴 **Направление: Курьерская доставка**\n\n"
        "• **Доход:** до 5 000 — 9 000 ₽ за смену\n"
        "• **Выплаты:** ежедневно или еженедельно на карту\n"
        "• **График:** полностью свободный (смены от 2-4 часов)\n"
        "• **Формат:** пешком, на велосипеде, самокате или личном авто\n"
        "• Бесплатная экипировка и термосумка\n\n"
        "Нажмите кнопку ниже для быстрой регистрации 👇",
        reply_markup=get_courier_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "cat_truck")
async def show_truck_vacancies(callback: CallbackQuery):
    await callback.message.edit_text(
        "🚛 **Направление: Грузовой курьер / Водитель**\n\n"
        "• **Доход:** высокий доход за заказ / рейс\n"
        "• **Формат:** на собственном или арендованном грузовом авто (каблук, фургон, Газель)\n"
        "• **Выплаты:** моментальный вывод средств\n"
        "• Подходит для работы в свободном режиме\n\n"
        "Нажмите кнопку ниже для отправки заявки 👇",
        reply_markup=get_truck_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "cat_warehouse")
async def show_warehouse_vacancies(callback: CallbackQuery):
    await callback.message.edit_text(
        "📦 **Направление: Склад / Комплектация (Яндекс Лавка)**\n\n"
        "• **Доход:** до 100 000 — 150 000 ₽ в месяц\n"
        "• **Условия:** работа в тёплом помещении у дома, без разъездов по улице\n"
        "• **Обязанности:** сборка и комплектация заказов\n"
        "• **Бонусы:** удобные графики, корпоративные скидки и бесплатное обучение\n\n"
        "Нажмите кнопку ниже для подачи заявки 👇",
        reply_markup=get_warehouse_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery):
    faq_text = (
        "❓ **Часто задаваемые вопросы:**\n\n"
        "1. **Берут ли без опыта?**\n"
        "— Да, всему обучают в первый день.\n\n"
        "2. **Когда приходят деньги?**\n"
        "— Вывод доступен на любую банковскую карту сразу после выполнения смен/заказов.\n\n"
        "3. **Сколько часов нужно работать?**\n"
        "— Вы сами выбираете время и дни выхода."
    )
    await callback.message.edit_text(faq_text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "support")
async def show_support(callback: CallbackQuery):
    support_text = (
        "💬 **Поддержка куратора**\n\n"
        "Если у вас есть вопросы по оформлению или выходу на смену:\n"
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
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
