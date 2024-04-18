from aiogram import types
from create_bot import dp
import sqlite3 

@dp.message_handler(content_types=types.ContentTypes.ANY, run_task=True)
async def process_message(message: types.Message):
    user_id = message.from_user.id
    chat_type = message.chat.type
    if chat_type not in ['group', 'supergroup']:
        return
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute('SELECT selfie_with_car FROM user_info WHERE id = ? AND selfie_with_car IS NOT NULL', (user_id,))
    row = cursor.fetchone()
    print(row)
    conn.close()
    if row:
        return
    else:
        await message.delete()




# @dp.message_handler(content_types=types.ContentTypes.ANY, run_task=True)
# async def process_message(message: types.Message):
#     user_id = message.from_user.id
#     chat_type = message.chat.type
#     if chat_type not in ['group', 'supergroup']:
#         return
#     conn = sqlite3.connect('user_info.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT check_done FROM user_info WHERE id = ?', (user_id,))
#     row = cursor.fetchone()
#     print(row)
#     conn.close()
#     if row is not True:
#         await message.delete()
        
