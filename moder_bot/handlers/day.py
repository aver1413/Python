from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from create_bot import dp, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo



                            



inl = InlineKeyboardMarkup (row_width=1).add(InlineKeyboardButton(text='Отправить ежедневный отчёт', web_app=WebAppInfo(url=f'')))




@dp.message_handler(commands='day')
async def inline(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбери действие', reply_markup=inl)
