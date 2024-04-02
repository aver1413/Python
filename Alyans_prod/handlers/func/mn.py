from aiogram import types
from create_bot import dp, bot
from keyboards.spec_kb import kb_spec
import sqlite3

CHANNEL_ID = -10018053526


@dp.message_handler(commands='mn')
async def mn(message: types.Message):
    await bot.send_message(CHANNEL_ID, f'@{message.from_user.username} перешёл в меню')
    user_id = message.from_user.id
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM spec')
    rows = cur.fetchall()
    username_spec = [row[0] for row in rows]
    if message.from_user.username in username_spec:
        await message.delete()
        await bot.send_message(user_id, 'Меню специалиста', reply_markup=kb_spec)
        # await message.answer('Меню специалиста', reply_markup=kb_spec)
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к боту
Для его получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")