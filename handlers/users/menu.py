
from ast import Call
from cgitb import text
from email import message
from pickletools import markobject
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from loader import dp, db, bot
from aiogram.types.chat import ChatActions
from keyboards.inline.products_from_cart import product_markup, product_cb
from aiogram.dispatcher import FSMContext
from loader import dp
from filters import IsAdmin, IsUser
from data import config
from aiogram import executor, types
from keyboards.inline.categories import categories_markup
from keyboards.default.markups import start_ad


user_message = '/user'
if config.ADMINS:
    admin_message = '/admin'


catalog = '🛍️ Каталог'
balance = '💬 Админа йозиш'
cart = '🛒 Сават'
delivery_status = '🚚 Буюртма ҳолати'

settings = '⚙️ Каталог созламалари'
orders = '🚚 Буюртмалар'
questions = '❓ Саволлар'

@dp.message_handler(IsAdmin(), commands='start')
@dp.message_handler(IsAdmin(), commands='admin')
async def admin_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    cid = message.chat.id
    markup.add(settings)
    markup.add(questions, orders)
    markup.add(user_message)




    await message.answer('Меню', reply_markup=markup)

# @dp.message_handler(IsAdmin(), commands='start')
# @dp.message_handler(IsAdmin(), commands='')
@dp.message_handler(IsUser(), commands='start')
async def user_menu(message: Message):
    # markup = ReplyKeyboardMarkup(selective=True)
    cid = message.chat.id

    if cid in config.ADMINS:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(admin_message)
        markup.add(catalog)
        markup.add(balance, cart)
        markup.add(delivery_status)

    if cid not in config.ADMINS:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(catalog)
        markup.add(balance, cart)
        markup.add(delivery_status)
    


    await message.answer('''<b>Келинг, совғангизни бирга танлаймиз\n✌️</b>''', reply_markup=categories_markup())

@dp.callback_query_handler(text='back')
async def back_post(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer('''<b>Келинг, совғангизни бирга танлаймиз\n✌️</b>''', reply_markup=categories_markup())

@dp.callback_query_handler(text='about')
async def about_me(call: CallbackQuery):
    await call.message.answer('''"JAYHUN GULSHANI" 💯✨ ORGINAL✨.
UNUTILMAS ONLARINGIZNI JAYHUN GULSHANI BILAN TARIXGA MUHIRLANG 
BIZ TUG'ILGAN KUN ,TÕY va BAZMLARDA YAQINLARINGIZGA KUTILMAGAN SYURPRIZLARLAR ÕTKAZAMIZ.
🎂🎈🎀🎁🎇🧨🌹💐''')
