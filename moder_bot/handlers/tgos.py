from aiogram import types, Dispatcher
from create_bot import bot






# @dp.message_handler(commands='start')
async def tgos(message : types.Message):
    await message.delete()
    await message.answer(f'#TG\n@{message.from_user.username} сегодня на telegram аккаунте')
   


def tgos_handlers(dp : Dispatcher):
    dp.register_message_handler(tgos, commands='tgos')