
from aiogram import Bot, types
from create_bot import dp, bot
from keyboards.kb_main import kb_main


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, привет 👋\nВыбери в меню действие 👇', reply_markup=kb_main)