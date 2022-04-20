
from aiogram.types import Message
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from handlers.users.menu import orders
from data.config import ADMINS, CHANNELS
from filters import IsAdmin

@dp.message_handler(IsAdmin(), text=orders)
async def process_orders(message: Message):
    
    orders = db.fetchall('SELECT * FROM orders')
    
    if len(orders) == 0: await message.answer('Сизда буюртма йоқ.')
    else: await order_answer(message, orders)

async def order_answer(message, orders):
    



    res = f" "
    # res += f"boshi: {orders[1]}\n"
    # res += f"ismi: {orders[5]}\n"
    # res += f"nomer: {}\n"
    # res += f"adress: {orders[2]}\n"
    # await bot.message.answer("Adminga jo'natildi", show_alert=True)
    # for i in ADMINS:
    #     await bot.send_message(i, res)
    #     await message.edit_reply_markup()





    for order in orders:
        res = f'Буюртма <b>+{order[3]}\nIsm: {order[1]}\nAddres: {order[2]}\n----\n</b>'

        

        await message.answer(res)   
        # for i in res:
        #     await bot.send_message(i, res)
        # message = await message.edit_reply_markup()

    await message.send_copy(chat_id=CHANNELS[0])

