import gspread
from google.oauth2.service_account import Credentials
from aiogram import Bot, types
from create_bot import dp, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from time import sleep
import sqlite3


CHANNEL_ID = -10018053526

# Указываем данные вашего Google аккаунта и ключ сервисного аккаунта
credentials = Credentials.from_service_account_file('hermal-pattern-394314-c98e9373fa4c.json', scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('')
worksheet = spreadsheet.worksheet('Price')







@dp.message_handler(commands='price')
async def opros2(message: types.Message):
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM spec')
    rows = cur.fetchall()
    username_spec = [row[0] for row in rows]
    if message.from_user.username in username_spec:
        await message.delete()
        credentials = Credentials.from_service_account_file('hermal-pattern-394314-c98e9373fa4c.json', scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
        client = gspread.authorize(credentials)
        spreadsheet = client.open_by_key('')
        worksheet = spreadsheet.worksheet('Price')
        cell_value = worksheet.acell("A1").value
        await bot.send_message(CHANNEL_ID, f'@{message.from_user.username} смотрит цены на оборудование / тарифы')
        await bot.send_message(message.from_user.id, cell_value, parse_mode='html')
        global id_user
        id_user = message.from_user.id
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к боту
Для его получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")



