from aiogram import types, Dispatcher
from create_bot import bot, dp
import sqlite3
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

CHANNEL_ID = -1001

CHANNEL_ID_GROUP = -100162



inkb2 = InlineKeyboardMarkup (row_width=1).add(InlineKeyboardButton(text='Да', callback_data='news_yes22')).add(InlineKeyboardButton(text='Нет', callback_data='news_no22'))


class FSMAdmin(StatesGroup):
    photo = State()
    sendnews2 = State()


async def send_mini_news_photo(message : types.Message):
    await FSMAdmin.photo.set()
    global setuser
    setuser = message.from_user.id
    await message.answer("Отправь скриншот")

   

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=FSMAdmin.photo)
async def forward_photo(message: types.Message):
    await FSMAdmin.sendnews2.set()
    # Получаем информацию о фото
    global photo
    photo = message.photo[-1]
    await bot.send_message(setuser, 'Теперь напиши новость')




@dp.message_handler(state=FSMAdmin.sendnews2)
async def send_new_done(message: types.Message, state: FSMContext):
    global news2, text_news2
    news2 = message.text
    text_news2 = await bot.send_photo(setuser, photo=photo.file_id, caption=f'Твоя мини-новость, верно?\n{news2}', reply_markup=inkb2)
    await state.finish()



@dp.callback_query_handler(text='news_yes22')
async def news_yes(callback : types.CallbackQuery):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=text_news2.message_id)
    await callback.answer("Отправил новость", show_alert=True)
    await callback.answer()
    text_news_group = f'🗞 Уведомление Альянса 🗞\n\n{news2}'
    await bot.send_photo(CHANNEL_ID_GROUP, photo=photo.file_id, caption=text_news_group)
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT ID FROM ID')
    users = cur.fetchall()
    sendusers = cur.execute('SELECT USERNAME FROM ID').fetchall()
    count_users = len(sendusers)
    sorted_list = sorted(sendusers, key=lambda x: x[0])
    username_senduser = "\n".join("@" + item[0] for item in sorted_list)
    for user_id in users:
        chat_id = int(user_id[0])
        global text_news
        text_news = f'🗞 Уведомление Альянса 🗞\n\n{news2}'
        await bot.send_photo(chat_id, photo=photo.file_id, caption=text_news, parse_mode='html')
    await bot.send_message(setuser, f'Уведомление получили[{count_users}]:\n{username_senduser}')

        




@dp.callback_query_handler(text='news_no22')
async def news_yes(callback : types.CallbackQuery):
    await callback.answer("Ок, отменим", show_alert=True)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=text_news2.message_id)
    
 








