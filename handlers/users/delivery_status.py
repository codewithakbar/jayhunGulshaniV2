
from aiogram.types import Message
from loader import dp, db
from .menu import delivery_status
from filters import IsUser
from aiogram.types import Message, CallbackQuery
from keyboards.inline.products_from_catalog import back_to_menu
from .newpost import image

@dp.message_handler(IsUser(), text=delivery_status)
@dp.callback_query_handler(text='state_cart')
async def main():
    image()
# async def process_delivery_status(call: CallbackQuery):
    
#     orders = db.fetchall('SELECT * FROM orders WHERE cid=?', (call.message.chat.id,))
    
#     if len(orders) == 0: await call.message.answer('Сизда фаол буюртмалар йоқ.')
#     else: await delivery_status_answer(call.message, orders)

# async def delivery_status_answer(orders, call: CallbackQuery):

#     res = ''

#     for order in orders:
#         p = '-' * 60
#         res += f' <b>{order[1]}нинг Закази:</b> <b>\n{p}\n№: {order[5]}\n{p}\nIsm: {order[1]}\n{p}\nAdres: {order[2]}\n{p}\nTelefon: {order[3]}\n{p}\nLocatsiya: {order[4]}\n\n</b>'
#         answer = [
#             '<b>заказ мавжуд.</b>',
#             ' йолда!',
#             ' келди ва сизни почтада кутмоқда!'
#         ]

#         res += answer[0]
#         res += '\n\n'

#     await call.message.answer(res, reply_markup=back_to_menu())

# if __name__ == '__main__':
    # main()

