from aiogram import Bot, types
from create_bot import dp, bot
import sqlite3
from datetime import date
from datetime import timedelta
from datetime import datetime, timedelta
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdmin(StatesGroup):
    вопрос5 = State()
    
channel_id = -1002

@dp.message_handler(text='Проверить специалиста')
async def gotov(message: types.Message, state=None):
    await bot.send_message(message.from_user.id, 'Введи фамилию и имя\nПример: Аверьянов Евгений')
    await FSMAdmin.next()

@dp.message_handler(state=FSMAdmin.вопрос5)
async def v5(message: types.Message, state: FSMContext):
        global name
        name = message.text
        await state.finish()
        await bot.send_message(channel_id, f'#логи\n@{message.from_user.username} проверил специалиста "{name}" на кол-во нажатий причин')
        await mon(message)
        



async def mon(message: types.Message):
    try:
        base = sqlite3.connect('stat.db')
        cur = base.cursor()

        query = f"SELECT COUNT(*) FROM data WHERE name = '{name}'"
        cur.execute(query)
        count_rows = cur.fetchone()[0]

        await message.answer(f"{name} зафиксировал - {count_rows} причин")

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

    finally:
        base.close()
                
            
        


    
      



