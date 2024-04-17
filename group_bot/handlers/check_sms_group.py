from aiogram import types
from create_bot import dp, bot

@dp.message_handler(content_types=types.ContentTypes.ANY, run_task=True)
async def check_user(message: types.Message):
    user_id = message.from_user.id
    chat_type = message.chat.type
    if chat_type not in ['group', 'supergroup']:
        return
    with open('ver.txt', 'r') as file:
        verified_users = file.read().splitlines()
    if str(user_id) not in verified_users:
        await message.delete()
        
