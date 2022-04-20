from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from loader import db

category_cb = CallbackData('category', 'id', 'action')

admin = '✍️ Админга ёзиш'
about = 'ℹ️ Биз ҳақимизда'
holat = 'Буюртма ҳолати📜'
savat = '🛒 Саватча'

def categories_markup():

    global category_cb
    
    markup = InlineKeyboardMarkup()
    for idx, title in db.fetchall('SELECT * FROM categories'):
        markup.add(InlineKeyboardButton(title, callback_data=category_cb.new(id=idx, action='view')))

    # markup.add(InlineKeyboardButton(text="✅ Adminga yozish", callback_data="to_admin"))
    markup.add(
        InlineKeyboardButton(text="✍️ Админга ёзиш", callback_data="to_admin"),
        # InlineKeyboardButton(text="Буюртма ҳолати📜", callback_data="state_cart"),   
    )
    markup.add(
        InlineKeyboardButton(text="ℹ️ Биз ҳақимизда", callback_data="about"),
        InlineKeyboardButton(text="🛒 Саватча", callback_data="cart_product"), 
    )


    return markup

