import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Токен бота от @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "ВАШ_ТОКЕН_БОТА_СЮДА")

# Ссылки на партнерские офферы
LINK_EDA = "https://trk.ppdu.ru/click/lRpy1nrx?erid=CQH36pWzJqVGXC5oLP8WVVNCNqJmbhiUPijGiu4zpwPd7G"
LINK_TRUCK = "https://trk.ppdu.ru/click/AZv8hynP?erid=CQH36pWzJqVGXC5oTTDpMBk8ei82kpZxV9ZJ1ZC292TAKx"
LINK_LAVKA = "https://trk.ppdu.ru/click/1F5Kat49?erid=CQH36pWzJqVGXC5oUHvq1FTH2g3oi1KL72bsqkyo9iVXM7"
LINK_CURATOR = "https://t.me/bystrosmena"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главная клавиатура
def main_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🍔 Курьер (пеший / вело / авто)", callback_data="vac_eda")
    builder.button(text="📦 Склад / Комплектовщик", callback_data="vac_lavka")
    builder.button(text="🚚 Грузовой авто (водитель)", callback_data="vac_truck")
    builder.button(text="❓ Частые вопросы (FAQ)", callback_data="menu_faq")
    builder.button(text="👤 Связаться с куратором", url=LINK_CURATOR)
    builder.adjust(1)
    return builder.as_markup()

# Кнопка возврата в меню
def back_kb(target_link=None, btn_text="👉 Подать заявку онлайн"):
    builder = InlineKeyboardBuilder()
    if target_link:
        builder.button(text=btn_text, url=target_link)
    builder.button(text="⬅️ Назад в меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()

# Меню FAQ
def faq_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="1. Нужен ли опыт работы?", callback_data="faq_exp")
    builder.button(text="2. Когда приходят первые выплаты?", callback_data="faq_pay")
    builder.button(text="3. Сколько стоит форма и сумка?", callback_data="faq_kit")
    builder.button(text="4. Можно ли совмещать с учёбой?", callback_data="faq_time")
    builder.button(text="⬅️ Назад в меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    text = (
        "👋 **Добро пожаловать в сервис «Быстро Смена»!**\n\n"
        "Я виртуальный куратор. Помогу подобрать проверенную работу или подработку "
        "рядом с домом с ежедневными выплатами.\n\n"
        "📍 Без комиссий, прямое официальное оформление.\n\n"
        "**Выберите интересующее направление:**"
    )
    await message.answer(text, reply_markup=main_kb(), parse_mode="Markdown")

@dp.callback_query(F.data == "main_menu")
async def back_to_main(call: types.CallbackQuery):
    text = (
        "💼 **Главное меню вакансий «Быстро Смена»**\n\n"
        "Выберите направление, чтобы узнать условия и подать онлайн-заявку:"
    )
    await call.message.edit_text(text, reply_markup=main_kb(), parse_mode="Markdown")
    await call.answer()

# Вакансия: Курьер
@dp.callback_query(F.data == "vac_eda")
async def vacancy_eda(call: types.CallbackQuery):
    text = (
        "🍔 **Курьер сервиса доставок**\n\n"
        "💰 **Доход:** до 11 000 ₽ / смену (ежедневно на карту)\n\n"
        "• **Формат:** пешком, велосипед, электросамокат или авто\n"
        "• **График:** полностью свободный (смены от 2 часов)\n"
        "• **Плюсы:** бесплатная форма и термосумка, чаевые 100% ваши\n"
        "• **Возраст:** от 18 лет (в ряде городов с 16 лет)\n\n"
        "Оформление занимает 2 минуты со смартфона 👇"
    )
    await call.message.edit_text(text, reply_markup=back_kb(LINK_EDA, "👉 Оформить анкету курьера"), parse_mode="Markdown")
    await call.answer()

# Вакансия: Склад
@dp.callback_query(F.data == "vac_lavka")
async def vacancy_lavka(call: types.CallbackQuery):
    text = (
        "📦 **Кладовщик-комплектовщик (тёплый склад)**\n\n"
        "💰 **Доход:** до 150 000 ₽ / мес (в регионах до 100 000 ₽)\n\n"
        "• **Условия:** работа в помещении у дома, без доставок по улице\n"
        "• **График:** сменный 5/2 (по 8 часов)\n"
        "• **Бонусы:** бесплатное такси до дома при вечерней смене, комплексные обеды за 95 ₽, ДМС и медкнижка за 0 ₽\n\n"
        "Нажмите кнопку ниже для отправки анкеты 👇"
    )
    await call.message.edit_text(text, reply_markup=back_kb(LINK_LAVKA, "👉 Подать заявку на склад"), parse_mode="Markdown")
    await call.answer()

# Вакансия: Грузовой
@dp.callback_query(F.data == "vac_truck")
async def vacancy_truck(call: types.CallbackQuery):
    text = (
        "🚚 **Водитель грузового транспорта**\n\n"
        "💰 **Доход:** до 337 000 ₽ / мес\n\n"
        "• **Формат:** свой грузовой авто или аренда (от каблука до Газели)\n"
        "• **Категории прав:** B или C\n"
        "• **Выплаты:** моментальный вывод средств на любую карту\n"
        "• **Плюсы:** страховка жизни и груза на каждом рейсе\n\n"
        "Перейдите к онлайн-регистрации авто 👇"
    )
    await call.message.edit_text(text, reply_markup=back_kb(LINK_TRUCK, "👉 Зарегистрировать авто"), parse_mode="Markdown")
    await call.answer()

# Раздел FAQ
@dp.callback_query(F.data == "menu_faq")
async def open_faq(call: types.CallbackQuery):
    text = "❓ **Частые вопросы соискателей:**\n\nВыберите интересующий вопрос:"
    await call.message.edit_text(text, reply_markup=faq_kb(), parse_mode="Markdown")
    await call.answer()

@dp.callback_query(F.data == "faq_exp")
async def faq_exp(call: types.CallbackQuery):
    text = (
        "❓ **Нужен ли опыт работы?**\n\n"
        "Опыт не требуется! Обучение и понятный видеоинструктаж проходят прямо в приложении за 15 минут. Выйти на первый слот можно сразу после регистрации."
    )
    await call.message.edit_text(text, reply_markup=back_kb(), parse_mode="Markdown")
    await call.answer()

@dp.callback_query(F.data == "faq_pay")
async def faq_pay(call: types.CallbackQuery):
    text = (
        "❓ **Когда приходят первые выплаты?**\n\n"
        "Деньги перечисляются ежедневно (при самозанятости) или раз в неделю прямо на карту любого банка РФ без скрытых сборов и вычетов."
    )
    await call.message.edit_text(text, reply_markup=back_kb(), parse_mode="Markdown")
    await call.answer()

@dp.callback_query(F.data == "faq_kit")
async def faq_kit(call: types.CallbackQuery):
    text = (
        "❓ **Сколько стоит форма и сумка?**\n\n"
        "Абсолютно 0 рублей! Комплект одежды по сезону и термосумка выдаются бесплатно в сервисном центре без залогов и удержаний из зарплаты."
    )
    await call.message.edit_text(text, reply_markup=back_kb(), parse_mode="Markdown")
    await call.answer()

@dp.callback_query(F.data == "faq_time")
async def faq_time(call: types.CallbackQuery):
    text = (
        "❓ **Можно ли совмещать с учёбой или работой?**\n\n"
        "Да, вы сами планируете график: слоты длятся от 2 часов. Можно выходить только вечером, в свободные от пар часы или по выходным дням."
    )
    await call.message.edit_text(text, reply_markup=back_kb(), parse_mode="Markdown")
    await call.answer()

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен и готов к приему сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
