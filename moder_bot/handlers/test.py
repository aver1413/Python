from aiogram import types, Dispatcher







# @dp.message_handler(commands='start')
async def checkwork(message : types.Message):
    await message.delete()
    await message.answer('Все функции работают исправно')   


def checkwork_handlers(dp : Dispatcher):
    dp.register_message_handler(checkwork, commands='ch')