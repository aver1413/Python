from aiogram import executor
from create_bot import dp




from handlers import start, send_lastday, stattekmon, statsetperiod, excel, check_spec



async def on_startup(_):
    print("Бот  запущен")






executor.start_polling(dp, skip_updates=True, on_startup=on_startup)