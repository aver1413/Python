from aiogram import types, Dispatcher
from create_bot import bot






# @dp.message_handler(commands='help')
async def help(message : types.Message):
    await message.answer("""Инструкция:
После каждого своего ответа необходимо прислать в бота скриншот своего ответа
Сделать это можно через команду /ot
Её также можно найти в кнопках Меню""")
    await message.delete()
   


def help_handlers(dp : Dispatcher):
    dp.register_message_handler(help, commands='help')