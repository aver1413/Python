from aiogram import Bot, types
from create_bot import dp, bot


from handlers.func.my_profile import my_profile

async def back():
    await my_profile()