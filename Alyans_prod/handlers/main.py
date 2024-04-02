from aiogram import types, Dispatcher
from create_bot import bot
from time import sleep
import sqlite3
from handlers.stager import stager_start
from handlers.spec import start_spec
from handlers.admin import start_admin

CHANNEL_ID = -1001805




async def start(message : types.Message):
    await message.delete()
    photo = "https://i.ibb.co/HFm6X6J/L-logo.jpg"
    await bot.send_photo(message.from_user.id, photo=photo, caption='''Добро пожаловать в Альянс 😎
Тут ты сможешь узнавать много полезной информации, а также пользоваться удобными функциями 😉''')
    await bot.send_message(CHANNEL_ID, f"{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} подключился к боту")
    global id
    id = message.from_user.id
    global user
    user = message.from_user.username
    global firstname
    firstname = message.from_user.first_name
    global lastname
    lastname = message.from_user.last_name
    message = await bot.send_message(id, 'Проверяю твой доступ [25%]')
    sleep(0.8)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    messag = await bot.send_message(id, 'Проверяю твой доступ [50%]')
    sleep(0.8)
    await bot.delete_message(chat_id=message.chat.id, message_id=messag.message_id)
    messa = await bot.send_message(id, 'Проверяю твой доступ [75%]')
    sleep(0.8)
    await bot.delete_message(chat_id=message.chat.id, message_id=messa.message_id)
    mess = await bot.send_message(id, 'Проверяю твой доступ [100%]')
    sleep(0.8)
    await bot.delete_message(chat_id=message.chat.id, message_id=mess.message_id)
    await bot.send_message(id, 'Данные загружены')
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT login FROM stager')
    rows = cur.fetchall()
    username_stager = [row[0] for row in rows]
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM spec')
    rows = cur.fetchall()
    username_spec = [row[0] for row in rows]
    if user in username_stager:
        await bot.send_message(id, "Ещё раз добро пожаловать в бота 😎", parse_mode="HTML")
        sleep(3)
        await stager_start(message)
        await bot.send_message(CHANNEL_ID, f"@{user} прошёл авторизацию по доступу. \nДоступ - <b>Стажировка</b>", parse_mode="HTML")
        base = sqlite3.connect('main.db')
        cur = base.cursor()
        cur.execute('INSERT OR IGNORE INTO ID VALUES(?, ?, ?, ?)', (int(id),(user),(firstname),(lastname)))
        base.commit()
        base.close()
    elif user in username_spec:
        await bot.send_message(id, "Ещё раз добро пожаловать в бота 😎", parse_mode="HTML")
        await start_spec(message)
        await bot.send_message(CHANNEL_ID, f"@{user} прошёл авторизацию по доступу. \nДоступ - <b>Специалист</b>", parse_mode="HTML")
    else:
        await message.answer(f"""Увы, у тебя нет доступа к боту
Для его получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")
        await bot.send_message(CHANNEL_ID, f"@{user} попробовал прорваться в бота, но доступа у него нет")
    base.close()



def start_handlers(dp : Dispatcher):
    dp.register_message_handler(start, commands='start')








