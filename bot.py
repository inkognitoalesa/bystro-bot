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
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
