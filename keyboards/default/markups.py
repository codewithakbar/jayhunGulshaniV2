from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

back_message = '👈 Оркага'
confirm_message = '✅ Заказ тастиклаш'
all_right_message = '✅ Хаммаси тогри'
cancel_message = '🚫 Бекор килиш'

admin = '✍️ Админга ёзиш'
about = 'ℹ️ Биз ҳақимизда'
holat = 'Буюртма ҳолати📜'
savat = '🛒 Саватча'

locate = '📍 Локация юбориш'

def confirm_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(confirm_message)
    markup.add(back_message)

    return markup

def back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(back_message)

    return markup

def check_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(back_message, all_right_message)

    return markup

def submit_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(cancel_message, all_right_message)

    return markup

def start_ad():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(admin, holat)
    markup.row(about, savat)

    return markup


def geo():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    return keyboard

