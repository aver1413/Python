import gspread
from google.oauth2.service_account import Credentials
from aiogram import Bot, types
from create_bot import dp, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from time import sleep
import sqlite3


CHANNEL_ID = -1001805352 

# Указываем данные вашего Google аккаунта и ключ сервисного аккаунта
credentials = Credentials.from_service_account_file('hermal-pattern-394314-c98e9373fa4c.json', scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('')
worksheet = spreadsheet.worksheet('Опрос')

# cell_value = worksheet.acell("A1").value


kb_opros_menu = InlineKeyboardMarkup (row_width=1).add(InlineKeyboardButton(text='Опрос', callback_data='opros')) \
.add(InlineKeyboardButton(text='Получить тест на 2 категорию', callback_data='2категория')) \





@dp.message_handler(text='🏫Обучение🏫')
async def opros2(message: types.Message):
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM spec')
    rows = cur.fetchall()
    username_spec = [row[0] for row in rows]
    if message.from_user.username in username_spec:
        await message.delete()
        await bot.send_message(CHANNEL_ID, f'@{message.from_user.username} перешёл в "Обучение"')
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, выбери то, что тебе нужно 😎', reply_markup=kb_opros_menu)
        global id_user
        id_user = message.from_user.id
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к боту
Для его получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")



@dp.callback_query_handler(text='opros')
async def check_opros(callback : types.CallbackQuery):
    username = callback.from_user.username
    await callback.bot.send_message(CHANNEL_ID, f'@{username} перешёл в "Опрос"')
    await callback.answer()
    cell_value = worksheet.acell("A2").value
    if cell_value == "TRUE":
        # await bot.send_message(message.from_user.id, "Пройдем опрос")
        cell_value_link = worksheet.acell("B2").value
        kb_opros = InlineKeyboardMarkup (row_width=1).add(InlineKeyboardButton(text='Пройти опрос', web_app=WebAppInfo(url=f'{cell_value_link}')))
        opr = await bot.send_message(id_user, "Выбери действие", reply_markup=kb_opros)
        sleep(10)
        await bot.delete_message(opr.chat.id, opr.message_id)
    elif cell_value == "FALSE":
        await bot.send_message(id_user, "В данный момент опрос не проходит 😔")



file_kat = 'Тест на 2 категорию SL1.docx'
file_2kat = 'Тест на 2 категорию SL2.docx'


@dp.callback_query_handler(text='2категория')
async def check_opros(callback : types.CallbackQuery):
    await callback.answer()
    with open(file_kat, 'rb') as document:
        await bot.send_document(id_user, document=document)
    with open(file_2kat, 'rb') as document:
        await bot.send_document(id_user, document=document)





    

