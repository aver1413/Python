from aiogram import types
from create_bot import dp, bot
from keyboards.spec_kb import kb_spec
import sqlite3
from time import sleep

CHANNEL_ID = -1001805352641 # Альянс admin-log
gif_wait = 'https://media1.tenor.com/m/1vXRFJxqIVgAAAAC/waiting-waiting-patiently.gif'

@dp.message_handler(commands='1')
async def check_user(message: types.Message):
    await bot.send_animation(message.from_user.id, gif_wait)
    id = message.from_user.id
    user = message.from_user.username
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM spec')
    rows = cur.fetchall()
    username_spec = [row[0] for row in rows]
    if message.from_user.username in username_spec:
        await message.delete()
        base = sqlite3.connect('main.db')
        cur = base.cursor()
        cur.execute('INSERT OR IGNORE INTO ID VALUES(?, ?, ?, ?)', (int(id),(user),(firstname),(lastname)))
        base.commit()
        sleep(2)
        await bot.send_message(message.from_user.id, "🙏 Спасибо за подтверждение авторизации 🙏")
        users = cur.execute('SELECT USERNAME FROM ID').fetchall()
        count_users = len(users)
        sorted_list = sorted(users, key=lambda x: x[0])
        username_users = "\n".join("@" + item[0] for item in sorted_list)
        await bot.send_message(CHANNEL_ID, f"""#сheck\n@{message.from_user.username} {message.from_user.first_name} {message.from_user.last_name} подтвердил своё присутствие в боте
Пользователей в боте = {count_users}
<b><i>Пользователи:</i></b>
{username_users}""", parse_mode='html')
        base.close()
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к боту
Для его получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")