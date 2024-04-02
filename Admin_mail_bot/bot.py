from aiogram import executor
from create_bot import dp
import sqlite3
from data_base import sqlite
from handlers import start


async def on_startup(_):
    print("Бот Альянса запущен")
sqlite.sql_start()



async def on_startup(_):
    print("Бот запущен")


start.start_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)