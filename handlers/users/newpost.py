from audioop import add
from loader import dp, bot
from aiogram import types
from states.newpost import NewPost
from aiogram.dispatcher import FSMContext
from keyboards.inline.manage import confirmation_keyboard
import logging
from cgitb import html, text
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.products_from_cart import product_markup, product_cb
from keyboards.inline.products_from_catalog import back_to_menu
from aiogram.utils.callback_data import CallbackData
from keyboards.default.markups import *
from aiogram.types.chat import ChatActions
from states import CheckoutState
from loader import dp, db, bot
from filters import IsUser
from .menu import cart
from aiogram import types
from data.config import ADMINS


# @dp.message_handler(IsUser(), text=cart)
@dp.callback_query_handler(text='cart_product')
async def process_cart(call: CallbackQuery, state: FSMContext):

            cart_data = db.fetchall(
                'SELECT * FROM cart WHERE cid=?', (call.message.chat.id,))

            if len(cart_data) == 0:

                await call.message.answer('Сизнинг саватчангиз бош.')

            else:

                await bot.send_chat_action(call.message.chat.id, ChatActions.TYPING)
                async with state.proxy() as data:
                    data['products'] = {}

                order_cost = 0

                for _, idx, count_in_cart in cart_data:

                    product = db.fetchone('SELECT * FROM products WHERE idx=?', (idx,))

                    if product == None:

                        db.fetchall('DELETE FROM cart WHERE idx=?', (idx,))

                    else:
                        _, title, body, image, price, _ = product
                        order_cost += price

                        async with state.proxy() as data:
                            data['products'][idx] = [title, price, count_in_cart]

                        markup = product_markup(idx, count_in_cart)
                        text = f'<b>{title}</b>\n\n{body}'

                        await call.message.answer_photo(photo=image,
                                                caption=text,
                                                reply_markup=markup)

                if order_cost != 0:
                    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    markup.add('📦 Буюртма бериш')

                    await call.message.answer('Ҳисоб-китобга ўтамизми?',
                                        reply_markup=markup)


@dp.callback_query_handler(IsUser(), product_cb.filter(action='count'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='increase'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='decrease'))
async def product_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):

    idx = callback_data['id']
    action = callback_data['action']

    if 'count' == action:

        async with state.proxy() as data:

            if 'products' not in data.keys():

                await process_cart(query.message, state)

            else:

                await query.answer('Миқдор - ' + data['products'][idx][2])

    else:

        async with state.proxy() as data:

            if 'products' not in data.keys():

                await process_cart(query.message, state)

            else:

                data['products'][idx][2] += 1 if 'increase' == action else -1
                count_in_cart = data['products'][idx][2]

                if count_in_cart == 0:

                    db.query('''DELETE FROM cart
                    WHERE cid = ? AND idx = ?''', (query.message.chat.id, idx))

                    await query.message.delete()
                else:

                    db.query('''UPDATE cart 
                    SET quantity = ? 
                    WHERE cid = ? AND idx = ?''', (count_in_cart, query.message.chat.id, idx))

                    await query.message.edit_reply_markup(product_markup(idx, count_in_cart))


# @dp.message_handler(text_contains="E'lon berish", state=None)
@dp.message_handler(text_contains="📦 Буюртма бериш", state=None)
async def new_post(message: types.Message):
    await message.answer("Буюрма бермоқчи бўлган махсулотингизни номини киритинг!")
    await NewPost.title.set()


@dp.message_handler(state=NewPost.title)
async def title(message: types.Message, state: FSMContext):
    title = message.text

    await state.update_data(
        {'title': title}
    )
    await message.answer("Маҳсулот ҳақида кушимча маълумот киритинг (ихтиёрий)")
    await NewPost.next()


@dp.message_handler(state=NewPost.desc)
async def title(message: types.Message, state: FSMContext):
    desc = message.text

    await state.update_data(
        {'desc': desc}
    )
    await message.answer("Маҳсулот нархини киритинг!")
    await NewPost.next()


@dp.message_handler(state=NewPost.price)
async def price(message: types.Message, state: FSMContext):
    price = message.text

    await state.update_data(
        {'price': price}
    )
    await message.answer("Телефон рақамингизни киритинг!")
    await NewPost.next()


@dp.message_handler(state=NewPost.phone)
async def phone_number(message: types.Message, state: FSMContext):
    phone = message.text

    await state.update_data(
        {'phone': phone}
    )

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)

    await message.answer("Буюртмангизни етказиб бериш учун манзилингизни юборинг!", reply_markup=keyboard)
    await NewPost.next()


# @dp.message_handler(content_types=["location"])
@dp.message_handler(state=NewPost.address)
async def procec_locate(message: types.Message, state: FSMContext):
    if message.location is not None:
        address = ("https://www.google.com/search?q=%s+%s" % (message.location.latitude, message.location.longitude))
    # address += message.location.longitude
    else:
        address = 'lokatsiya belgilamadi'
        
    await state.update_data(
        {'address': address}
    )

    # await message.answer("https://www.google.com/search?q=%s+%s" % (message.location.latitude, message.location.longitude))
    await message.answer("Энди буюртманинг расмини юборинг!")
    await NewPost.next()


@dp.message_handler(content_types=['photo'], state=NewPost.image)
async def image(message: types.Message, state: FSMContext):
    image = message.photo[-1].file_id

    await state.update_data(
        {'image': image}
    )
    # # Ma'lumotlarni qayta o'qiymiz
    data = await state.get_data()
    title = data.get('title')
    desc = data.get('desc')
    price = data.get('price')
    phone = data.get('phone')
    address = data.get('address')
    image = data.get('image')

    msg = "📄 <b>Quyidagi ma'lumotlar qabul qilindi:</b>\n\n"
    msg += f"Nomi: {title}\n"
    msg += f"Batafsil: {desc}\n\n"
    msg += f"Narxi: {price}\n"
    msg += f"Telefon raqam: {phone}\n"
    msg += f"Manzil: {address}\n"
    await message.answer_photo(image, caption=msg, reply_markup=confirmation_keyboard)
    await NewPost.next()

    # await state.finish()


