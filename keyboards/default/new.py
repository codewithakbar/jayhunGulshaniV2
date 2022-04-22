from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/start"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
