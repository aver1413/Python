from aiogram import types, Dispatcher
from create_bot import bot, dp
import sqlite3
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

CHANNEL_ID = -1001805
CHANNEL_ID_GROUP = -10016238



inkb = InlineKeyboardMarkup (row_width=1).add(InlineKeyboardButton(text='Ознакомился с новостью', callback_data='news'))
inkb2 = InlineKeyboardMarkup (row_width=1).add(InlineKeyboardButton(text='Да', callback_data='news_yes')).add(InlineKeyboardButton(text='Нет', callback_data='news_no'))


class FSMAdmin(StatesGroup):
    sendnews = State()



# @dp.message_handler(commands='send') # Отправка сообщения всем участникам бота
async def send_news(message: types.Message, state: FSMContext = None):
    await FSMAdmin.sendnews.set()
    await bot.send_message(message.from_user.id, 'Напиши новость')




@dp.message_handler(state=FSMAdmin.sendnews)
async def send_new_done(message: types.Message, state: FSMContext):
    global news
    news = message.text
    global text_news
    text_news = await bot.send_message(message.from_user.id, f'Твоя новость, верно?\n{news}', reply_markup=inkb2)
    await state.finish()



@dp.callback_query_handler(text='news_yes')
async def news_yes(callback : types.CallbackQuery):
    await callback.answer("Отправил новость", show_alert=True)
    await callback.answer()
    text_news_group = f'🗞 Новости Альянса 🗞\n\n{news}'
    await bot.send_message(CHANNEL_ID_GROUP, text_news_group, reply_markup=inkb)
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('INSERT INTO news VALUES(?)', (news, ))
    base.commit()
    base.close()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT ID FROM ID')
    users = cur.fetchall()
    for user_id in users:
        chat_id = int(user_id[0])
        global text_news
        text_news = f'🗞 Новости Альянса 🗞\n\n{news}'
        await bot.send_message(chat_id, text_news, reply_markup=inkb)
        




@dp.callback_query_handler(text='news_no')
async def news_yes(callback : types.CallbackQuery):
    await callback.answer("Ок, отменим", show_alert=True)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=text_news.message_id)
    
 



@dp.callback_query_handler(text='news')
async def call(callback : types.CallbackQuery):
    await callback.answer('Хорошо, молодец')
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
    await callback.bot.send_message(CHANNEL_ID, f'#news\n@{callback.from_user.username} {callback.from_user.first_name} {callback.from_user.last_name} ознакомился с новостью')
    





