from aiogram import types
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.spec_kb import kb_spec
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


CHANNAL_ID = -1001683754075 # Группа "Плохие звонки"



incancel = InlineKeyboardMarkup (row_width=1).add(InlineKeyboardButton(text='Да', callback_data='yes_bad_call')).add(InlineKeyboardButton(text='Передумал', callback_data='no_bad_call'))




class FSMAdmin(StatesGroup):
    ID = State()


async def start_bad_call(message: types.Message):
    from handlers.spec import ID
    global md
    md = await bot.send_message(ID, 'Хорошо 😎', reply_markup=ReplyKeyboardRemove())
    await bot.send_message(ID, 'Если ты хочешь разобрать звонок с тимлидом, нажми "Да" и отправь ID', reply_markup=incancel)
    



async def start_bad_call2(message: types.Message, state=None):
    from handlers.spec import ID
    await bot.send_message(ID, 'Хорошо 😎, пришли ID', reply_markup=ReplyKeyboardRemove())
    await FSMAdmin.next()
    


@dp.message_handler(state=FSMAdmin.ID)
async def load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.text
        text = message.text
        await bot.send_message(CHANNAL_ID, f'Специалист @{message.from_user.username} {message.from_user.first_name} {message.from_user.last_name} хочет разобрать звонок, ID - {text}')
    await state.finish()
    await bot.send_message(message.from_user.id, 'Зафиксировали, тимлид позовёт тебя', reply_markup=kb_spec)


    
@dp.callback_query_handler(text='yes_bad_call')
async def call(callback : types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await start_bad_call2(callback)


@dp.callback_query_handler(text='no_bad_call')
async def no_call(callback : types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await cmd_cancel(callback)



async def cmd_cancel(message: types.Message):
    await bot.send_message(message.from_user.id, 'Меню специалиста', reply_markup=kb_spec)
    