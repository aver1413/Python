from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards.spec_kb import kb_spec
import sqlite3
from time import sleep
from handlers.func.my_profile import my_profile
from handlers.func.helper import helper
from handlers.func.trener import trener_start
from handlers.func.bad_call import start_bad_call

CHANNEL_ID = -1001805

async def start_spec(message : types.Message):
    from handlers.main import id
    from handlers.main import user
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('INSERT OR IGNORE INTO ID VALUES(?, ?, ?, ?)', (int(id),(user),(id),(user)))
    base.commit()
    await bot.send_message(id, 'Меню специалиста', reply_markup=kb_spec)
    await bot.send_message(CHANNEL_ID, f"@{user} перешёл в меню специалиста", parse_mode="HTML")



async def start_spec2(message : types.Message):
    await bot.send_message(message.from_user.id, 'Меню специалиста', reply_markup=kb_spec)
    



@dp.message_handler(text='👨‍🏫Мой профиль👨‍🏫')
async def call_my_profile(message: types.Message):
    await my_profile(message)



@dp.message_handler(text='🆘HELPER🆘')
async def call_helper(message: types.Message):
    await helper(message)

@dp.message_handler(text='🗞Новости🗞')
async def check_news(message: types.Message):
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM spec')
    rows = cur.fetchall()
    username_spec = [row[0] for row in rows]
    if message.from_user.username in username_spec:
        base = sqlite3.connect('main.db')
        cur = base.cursor()
        cur.execute('SELECT NEWS FROM news')
        rows = cur.fetchall()
        news = [row[0] for row in rows]
        output = "\n_____________________________\n".join(news)
        await bot.send_message(message.from_user.id, output)
        await bot.send_message(CHANNEL_ID, f'@{message.from_user.username} перешёл в "Новости"')
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к этой функции
Для её получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")


@dp.message_handler(text='🥉Тренер🥉')
async def check_news(message: types.Message):
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM trener')
    rows = cur.fetchall()
    username_trener = [row[0] for row in rows]
    if message.from_user.username in username_trener:
        await trener_start(message)
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к этой функции
Для её получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")




@dp.message_handler(text='👎Плохой звонок👎')
async def check_news(message: types.Message):
    global ID
    ID = message.from_user.id
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM spec')
    rows = cur.fetchall()
    username_spec = [row[0] for row in rows]
    if message.from_user.username in username_spec:
        await start_bad_call(message)
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к этой функции
Для её получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")
































@dp.message_handler(text='Назад в меню специалиста')
async def back_in_menu_spec_helper(message: types.Message):
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM spec')
    rows = cur.fetchall()
    username_spec = [row[0] for row in rows]
    if message.from_user.username in username_spec:
        await start_spec2(message)
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к боту
Для её получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")
    

@dp.message_handler(text='Назад в меню')
async def back_in_menu_spec_trener(message: types.Message):
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM spec')
    rows = cur.fetchall()
    username_spec = [row[0] for row in rows]
    if message.from_user.username in username_spec:
        await start_spec2(message)
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к боту
Для её получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")
    


@dp.message_handler(text='Меню спеца')
async def back_in_menu_spec_trener(message: types.Message):
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await start_spec2(message)
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к боту
Для её получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")
    