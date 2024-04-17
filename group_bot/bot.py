from aiogram import executor
from create_bot import dp




from handlers import adm, start, check_sms_group, text



async def on_startup(_):
    print("Бот анкет запущен")






executor.start_polling(dp, skip_updates=True, on_startup=on_startup)