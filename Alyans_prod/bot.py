from aiogram import executor
from create_bot import dp
from data_base import sqlite



from handlers import main, stager, spec, admin
from handlers.func import news, opros, save_abon, konkors, gpt, news_mini, price, check, news_mini_photo, ouk
from handlers.func2 import hotkey

async def on_startup(_):
    print("Бот запущен")
sqlite.sql_start()


main.start_handlers(dp)




executor.start_polling(dp, skip_updates=True, on_startup=on_startup)