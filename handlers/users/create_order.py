from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
from data.config import ADMINS
from loader import dp, bot
from data.products import macbook, FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING
from keyboards.inline.product_keys import build_keyboard

@dp.message_handler(Command("macbook"))
async def show_invoices(message: types.Message):
    caption = "<b>Ноутбук Apple MacBook Air 2020 (2560x1600, Apple M1 3.2 ГГц, RAM 8 ГБ, SSD 256 ГБ, Apple graphics 7-core)</b>\n\n"
    caption += "Операционная система: macOS\n"
    caption += "Процессор: Apple M1 3.20 ГГц\nКоличество ядер процессора: 8\nОбъем кэша L2: 2 МБ\n"
    caption += "Экран: 13.3 дюймов, 2560x1600, широкоформатный\n"
    caption += "Общий объем накопителей SSD: 256 ГБ\n"
    caption += "Narxi: <b>11 608 500 сум</b>"
    await message.answer_photo(photo="https://bit.ly/3pYG7eV",
                         caption=caption, reply_markup=build_keyboard("macbook"))


@dp.callback_query_handler(text="product:macbook")
async def book_invoice(call: CallbackQuery):
    await bot.send_invoice(chat_id=call.from_user.id,
                           **macbook.generate_invoice(),
                           payload="payload:macbook")
    await call.answer()


@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Chet elga yetkazib bera olmaymiz")
    elif query.shipping_address.city.lower() == "urganch":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING],
                                        ok=True)

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Xaridingiz uchun rahmat!\n\nTez orada Admin siz bilan bo'glanadi😊")
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
                                f"ID: {pre_checkout_query.id}\n"
                                f"Telegram user: {pre_checkout_query.from_user.first_name}\n"
                                f"Xaridor: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}\n"
                                )
