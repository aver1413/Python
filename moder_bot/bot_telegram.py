from aiogram import executor
from create_bot import dp


from handlers import start, help, ot, tgos, test, day


async def on_startup(_):
    print("Бот запущен")


start.start_handlers(dp)
help.help_handlers(dp)
ot.ot_handlers(dp)
tgos.tgos_handlers(dp)
test.checkwork_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)