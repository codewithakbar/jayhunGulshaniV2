
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from data.config import ADMINS
from keyboards.default.markups import all_right_message, cancel_message, submit_markup, admin
from aiogram.types import Message
from states import SosState
from filters import IsUser
from loader import dp, db, bot


# @dp.message_handler(commands='sos')
@dp.callback_query_handler(text='to_admin')
async def cmd_sos(call: CallbackQuery):
    await SosState.question.set()
    await call.message.answer('Муаммонинг моҳияти нимада? Иложи борича батафсил тасвирлаб беринг, администратор сизга жавоб беради.', reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(state=SosState.question)
@dp.message_handler(state=SosState.question)
async def process_question(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text

    await message.answer('Ҳаммаси тўғри эканлигига ишонч ҳосил қилинг.', reply_markup=submit_markup())
    await SosState.next()


@dp.message_handler(lambda message: message.text not in [cancel_message, all_right_message], state=SosState.submit)
async def process_price_invalid(message: Message, call: CallbackQuery):
    await message.answer('Бундай вариант бўлмаган.')


@dp.message_handler(text=cancel_message, state=SosState.submit)
async def process_cancel(message: Message, state: FSMContext, call: CallbackQuery):
    await message.answer('Бекор қилинди!', reply_markup=ReplyKeyboardRemove())
    await state.finish()


# @dp.message_handler(text=all_right_message, state=SosState.submit)
@dp.message_handler(text=all_right_message, state=SosState.submit)
async def process_submit(message: Message, state: FSMContext):  

    cid = message.chat.id

    # if db.fetchone('SELECT * FROM questions WHERE cid=?', (cid,)) == None:

    async with state.proxy() as data:
        db.query('INSERT INTO questions VALUES (?, ?)',
                    (cid, data['question']))

    await message.answer('Юборилди!', reply_markup=ReplyKeyboardRemove())
    for i in ADMINS:
        gap = f"Yangi Savol, Admin panelida javob bering!"
        await message.answer(gap)
        await bot.send_message(message.chat.id, data['question'])
    
    # else:

    #     await message.answer('Берилган саволлар сони чегарасидан ошиб кетди.', reply_markup=ReplyKeyboardRemove())

    await state.finish()
