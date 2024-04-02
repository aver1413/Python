from aiogram import types, Dispatcher
from create_bot import bot






# @dp.message_handler(commands='start')
async def start(message : types.Message):
    await bot.send_message(message.from_user.id, "Добро пожаловать в бота \nДля отправки скрина - введи /ot")
   


def start_handlers(dp : Dispatcher):
    dp.register_message_handler(start, commands='start')