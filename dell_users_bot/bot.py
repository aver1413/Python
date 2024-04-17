import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from handlers.start import router



logging.basicConfig(level=logging.INFO)
bot = Bot(token="6742120409:AAGZ0fQaHz74UynIkef2cHOIEB-PDsspGJw")
dp = Dispatcher()




async def main():
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())