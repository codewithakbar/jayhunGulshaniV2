import middlewares, filters, handlers
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from loader import dp
from data import config
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands



user_message = '/user'
admin_message = '/admin'
catalog = '🛍️ Каталог'
balance = '💰 Баланс'
cart = '🛒 Сават'
delivery_status = '🚚 Буюртма ҳолати'


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):

    cid = message.chat.id
    if cid not in config.ADMINS:
        config.ADMINS.append(cid)

    await message.answer('Админ режими ёқилди. /start bo\'sing', reply_markup=ReplyKeyboardRemove())


if config.ADMINS:
    @dp.message_handler(text=user_message)
    async def user_mode(message: types.Message):

        cid = message.chat.id
        if cid in config.ADMINS:
            config.ADMINS.remove(cid)

        await message.answer('User режими ёқилди. /start bo\'sing', reply_markup=ReplyKeyboardRemove())



async def on_startup(dispatcher):
    # Birlamchi komandalar (/start va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
