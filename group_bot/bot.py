from aiogram import executor
from create_bot import dp




from handlers import start, check_sms_group, data, text



async def on_startup(_):
    print("Бот запущен")






executor.start_polling(dp, skip_updates=True, on_startup=on_startup)