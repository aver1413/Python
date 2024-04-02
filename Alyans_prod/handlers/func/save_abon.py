import gspread
from google.oauth2.service_account import Credentials
from aiogram import Bot, types
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardRemove
import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import kb_spec

class FSMAdmin(StatesGroup):
    ID2 = State()

# Указываем данные вашего Google аккаунта и ключ сервисного аккаунта
credentials = Credentials.from_service_account_file('hermal-pattern-394314-c98e9373fa4c.json', scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('')
worksheet = spreadsheet.worksheet('Лист')

# cell_value = worksheet.acell("A1").value




@dp.message_handler(text='💾Сохранил абонента💾')
async def opros2(message: types.Message):
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM spec')
    rows = cur.fetchall()
    username_spec = [row[0] for row in rows]
    if message.from_user.username in username_spec:
        await message.delete()
        global id_user
        id_user = message.from_user.id
        await save_abon1(message)
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к боту
Для его получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")



async def save_abon1(message: types.Message, state=None):
     await bot.send_message(id_user, 'Отправь ID', reply_markup=ReplyKeyboardRemove())
     await FSMAdmin.next()


spreadsheet = client.open_by_key('')
worksheet = spreadsheet.worksheet('Лист')

@dp.message_handler(state=FSMAdmin.ID2)
async def load22(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.text
        text = message.text
        all_values = worksheet.get_all_values()
        row_number = len(all_values) + 1
        column_number = 2  # Номер колонки, например, 2 для колонки B
        column_number1 = 1  # Номер колонки, например, 2 для колонки B
        worksheet.update_cell(row_number, column_number, text)
        worksheet.update_cell(row_number, column_number1, message.from_user.last_name)
        await bot.send_message(id_user, 'Зафиксировали, спасибо 😎', reply_markup=kb_spec)
    await state.finish()
    

