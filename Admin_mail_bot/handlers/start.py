from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import kb
import sqlite3
import pytz
from datetime import datetime

GIF1 = "https://media.tenor.com/qkuAZVkU2usAAAAd/bird-bird-of-prey.gif"
GIF2 = "https://media.tenor.com/3TnxpI_ML84AAAAC/bald-eagle.gif"
GIF3 = "https://media.tenor.com/LgLaEjPywWkAAAAd/eagle-logo.gif"

CHAT = -1
message_thread_id = 1

## await bot.send_message(CHAT, message_thread_id=message_thread_id, text = ##


async def start(message : types.Message):
    await bot.send_message(message.from_user.id, "Орёл прилетел или улетел?", reply_markup=kb)
    await bot.send_animation(message.from_user.id, GIF1)
    await message.delete()
   

async def tut(message: types.Message):
    await message.delete()
    await message.answer("Передали на отправку")
    username = message.from_user.username
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (login) VALUES (?)", (username,))
    cursor.execute("SELECT login FROM user GROUP BY login ORDER BY COUNT(*) DESC LIMIT 1")
    usertop = cursor.fetchone()[0]

    # Получение текущего времени в UTC+3
    timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(timezone)
    current_time = now.strftime('%H:%M')

    cursor.execute("INSERT INTO intime (time) VALUES (?)", (current_time,))
    cursor.execute("SELECT time FROM intime")
    times = cursor.fetchall()
    total_hours = sum(int(time[0].split(':')[0]) for time in times)
    total_minutes = sum(int(time[0].split(':')[1]) for time in times)
    total_time_in_minutes = total_hours * 60 + total_minutes
    average_time_in_minutes = total_time_in_minutes / len(times)
    hours = int(average_time_in_minutes / 60)
    minutes = int(average_time_in_minutes % 60)
    intime = f"{hours:02d}:{minutes:02d}"
    conn.commit()
    conn.close()
    print(usertop)
    print(intime)
    await bot.send_message(CHAT, message_thread_id=message_thread_id, text=f"❗️❗️❗️ATTENTION❗️❗️❗️\n❗️❗️❗️ОРЁЛ ВЛЕТЕЛ В ЗДАНИЕ❗️❗️❗️\nПочтальон - @{message.from_user.username}\nСреднее время прилёта: {intime}\nЧаще прилетающая сова от @{usertop}🦉")
    await bot.send_animation(CHAT, message_thread_id=message_thread_id, animation=GIF2)


async def netut(message: types.Message):
    await message.delete()
    await message.answer("Передали на отправку")
    username = message.from_user.username
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (login) VALUES (?)", (username,))
    cursor.execute("SELECT login FROM user GROUP BY login ORDER BY COUNT(*) DESC LIMIT 1")
    usertop = cursor.fetchone()[0]

    # Получение текущего времени в UTC+3
    timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(timezone)
    current_time = now.strftime('%H:%M')

    cursor.execute("INSERT INTO outtime (time) VALUES (?)", (current_time,))
    cursor.execute("SELECT time FROM outtime")
    times = cursor.fetchall()
    total_hours = sum(int(time[0].split(':')[0]) for time in times)
    total_minutes = sum(int(time[0].split(':')[1]) for time in times)
    total_time_in_minutes = total_hours * 60 + total_minutes
    average_time_in_minutes = total_time_in_minutes / len(times)
    hours = int(average_time_in_minutes / 60)
    minutes = int(average_time_in_minutes % 60)
    intime = f"{hours:02d}:{minutes:02d}"
    conn.commit()
    conn.close()
    print(usertop)
    print(intime)
    await bot.send_message(CHAT, message_thread_id=message_thread_id, text=f"❗️❗️❗️ATTENTION❗️❗️❗️\n❗️❗️❗️ОРЁЛ УЛЕТЕЛ ИЗ ЗДАНИЯ❗️❗️❗️\nПочтальон - @{message.from_user.username}\nСреднее время улёта: {intime}\nЧаще прилетающая сова от @{usertop}🦉")
    await bot.send_animation(CHAT, message_thread_id=message_thread_id, animation=GIF3)

async def oreltut(message : types.Message):
    await message.delete()
    username = message.from_user.username
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (login) VALUES (?)", (username,))
    cursor.execute("SELECT login FROM user GROUP BY login ORDER BY COUNT(*) DESC LIMIT 1")
    usertop = cursor.fetchone()[0]

    # Получение текущего времени в UTC+3
    timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(timezone)
    current_time = now.strftime('%H:%M')

    cursor.execute("INSERT INTO intime (time) VALUES (?)", (current_time,))
    cursor.execute("SELECT time FROM intime")
    times = cursor.fetchall()
    total_hours = sum(int(time[0].split(':')[0]) for time in times)
    total_minutes = sum(int(time[0].split(':')[1]) for time in times)
    total_time_in_minutes = total_hours * 60 + total_minutes
    average_time_in_minutes = total_time_in_minutes / len(times)
    hours = int(average_time_in_minutes / 60)
    minutes = int(average_time_in_minutes % 60)
    intime = f"{hours:02d}:{minutes:02d}"
    conn.commit()
    conn.close()
    print(usertop)
    print(intime)
    await bot.send_message(CHAT, message_thread_id=message_thread_id, text=f"❗️❗️❗️ATTENTION❗️❗️❗️\n❗️❗️❗️ОРЁЛ ВЛЕТЕЛ В ЗДАНИЕ❗️❗️❗️\nПочтальон - @{message.from_user.username}\nСреднее время прилёта: {intime}\nЧаще прилетающая сова от @{usertop}🦉")
    await bot.send_animation(CHAT, message_thread_id=message_thread_id, animation=GIF2)


async def orelnetut(message : types.Message):
    await message.delete()
    username = message.from_user.username
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (login) VALUES (?)", (username,))
    cursor.execute("SELECT login FROM user GROUP BY login ORDER BY COUNT(*) DESC LIMIT 1")
    usertop = cursor.fetchone()[0]

    # Получение текущего времени в UTC+3
    timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(timezone)
    current_time = now.strftime('%H:%M')

    cursor.execute("INSERT INTO outtime (time) VALUES (?)", (current_time,))
    cursor.execute("SELECT time FROM outtime")
    times = cursor.fetchall()
    total_hours = sum(int(time[0].split(':')[0]) for time in times)
    total_minutes = sum(int(time[0].split(':')[1]) for time in times)
    total_time_in_minutes = total_hours * 60 + total_minutes
    average_time_in_minutes = total_time_in_minutes / len(times)
    hours = int(average_time_in_minutes / 60)
    minutes = int(average_time_in_minutes % 60)
    intime = f"{hours:02d}:{minutes:02d}"
    conn.commit()
    conn.close()
    print(usertop)
    print(intime)
    await bot.send_message(CHAT, message_thread_id=message_thread_id, text=f"❗️❗️❗️ATTENTION❗️❗️❗️\n❗️❗️❗️ОРЁЛ УЛЕТЕЛ ИЗ ЗДАНИЯ❗️❗️❗️\nПочтальон - @{message.from_user.username}\nСреднее время улёта: {intime}\nЧаще прилетающая сова от @{usertop}🦉")
    await bot.send_animation(CHAT, message_thread_id=message_thread_id, animation=GIF3)




def start_handlers(dp : Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(tut, text='Орёл прилетел')
    dp.register_message_handler(oreltut, commands='oreltut')
    dp.register_message_handler(netut, text='Орёл улетел')
    dp.register_message_handler(orelnetut, commands='orelnetut')
    


