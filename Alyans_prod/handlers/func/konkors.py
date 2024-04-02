import gspread
from google.oauth2.service_account import Credentials
from aiogram import Bot, types
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardRemove
import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import kb_spec
from time import sleep
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton


CHANNEL_ID = -1001805352641 # Альянс admin-log


class FSMAdmin(StatesGroup):
    вопрос1 = State()
    вопрос2 = State()
    вопрос3 = State()
    вопрос4 = State()
    вопрос5 = State()
    вопрос6 = State()
    вопрос7 = State()
    вопрос8 = State()
    вопрос9 = State()
    вопрос10 = State()



# Указываем данные вашего Google аккаунта и ключ сервисного аккаунта
credentials = Credentials.from_service_account_file('hermal-pattern-394314-c98e9373fa4c.json', scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('')
worksheet = spreadsheet.worksheet('Анекты')

# cell_value = worksheet.acell("A1").value

spreadsheet1 = client.open_by_key('')
worksheet1 = spreadsheet1.worksheet('Лист')

async def check_konkurs(message: types.Message):
    cell_value = worksheet1.acell("A2").value
    if cell_value == "TRUE":
        await konkurs(message)
    elif cell_value == "FALSE":
        await bot.send_message(id_user, "В данный момент конкурс не проходит 😔")


@dp.message_handler(commands='конкурс')
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
        global firstname_user
        firstname_user = message.from_user.first_name
        global username
        username = message.from_user.username
        await check_konkurs(message)
    else:
        await bot.send_message(message.from_user.id, """Увы, у тебя нет доступа к боту
Для его получения обратись к тимлидам:
Евгений - @aver1413
Дмитрий - @Sselenso
Лев - @xphmi
""")

kb_check = InlineKeyboardMarkup (row_width=2).add(InlineKeyboardButton(text='Да, я готов', callback_data='Да, я готов')) \
.insert(InlineKeyboardButton(text='Нет, я передумал', callback_data='Нет, я передумал'))

async def konkurs(message: types.Message):
     global sms1
     sms1 = await bot.send_message(id_user, f"""
{firstname_user}, добро пожаловать на конкурс утренних чатеров 🥳""", reply_markup=ReplyKeyboardRemove())
     sleep(2)
     global sms2
     sms2 = await bot.send_message(id_user, """
Заполнение анкеты происходит через этого бота, но сначала ознакомься с условиями 👇""")
     sleep(2)
     global sms3
     sms3 = await bot.send_message(id_user, """
Условия:
1) У тебя должен """, reply_markup=kb_check)
     

@dp.callback_query_handler(text='Нет, я передумал')
async def check_opros(callback : types.CallbackQuery):
    await callback.answer()
    global chatid
    chatid = callback.message.chat.id
    await no_peredumal(callback)

async def no_peredumal(message: types.Message):
    await bot.send_message(id_user, 'Тогда забудем про всё это, если ты не против 😜\nЗахочешь попробовать еще раз ➡️ введи /конкурс и мы продолжим 😊', reply_markup=kb_spec)
    await bot.delete_message(chat_id=chatid, message_id=sms1.message_id)
    await bot.delete_message(chat_id=chatid, message_id=sms2.message_id)
    await bot.delete_message(chat_id=chatid, message_id=sms3.message_id)
    sleep(10)

    

@dp.callback_query_handler(text='Да, я готов')
async def check_opros(callback : types.CallbackQuery):
    await callback.answer()
    global chatid
    chatid = callback.message.chat.id
    await bot.delete_message(chat_id=chatid, message_id=sms3.message_id)
    await gotov(callback)


async def gotov(message: types.Message, state=None):
    await bot.send_message(id_user, 'Введи своё имя (Только Имя, фамилию пока что не надо 😁)')
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.вопрос1)
async def v1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global vo1
        vo1 = message.text
    await FSMAdmin.next()
    await bot.send_message(id_user, 'Теперь введи фамилию')


@dp.message_handler(state=FSMAdmin.вопрос2)
async def v2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global vo2
        vo2 = message.text
    await FSMAdmin.next()
    await bot.send_message(id_user, '')


@dp.message_handler(state=FSMAdmin.вопрос3)
async def v3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global vo3
        vo3 = message.text
    await FSMAdmin.next()
    await bot.send_message(id_user, '?')

@dp.message_handler(state=FSMAdmin.вопрос4)
async def v4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global vo4
        vo4 = message.text
    await FSMAdmin.next()
    await bot.send_message(id_user, '?')



@dp.message_handler(state=FSMAdmin.вопрос5)
async def v5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global vo5
        vo5 = message.text
    await FSMAdmin.next()
    await bot.send_message(id_user, '')



@dp.message_handler(state=FSMAdmin.вопрос6)
async def v6(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global vo6
        vo6 = message.text
    await FSMAdmin.next()
    await bot.send_message(id_user, '')


@dp.message_handler(state=FSMAdmin.вопрос7)
async def v7(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global vo7
        vo7 = message.text
    await FSMAdmin.next()
    await bot.send_message(id_user, '')



@dp.message_handler(state=FSMAdmin.вопрос8)
async def v8(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global vo8
        vo8 = message.text
    await FSMAdmin.next()
    await bot.send_message(id_user, '')


@dp.message_handler(state=FSMAdmin.вопрос9)
async def v9(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global vo9
        vo9 = message.text
    await FSMAdmin.next()
    await bot.send_message(id_user, '')

@dp.message_handler(state=FSMAdmin.вопрос10)
async def v9(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global vo10
        vo10 = message.text
    await state.finish()
    await load223(message)



spreadsheet = client.open_by_key('')
worksheet = spreadsheet.worksheet('Анекты')


async def load223(message: types.Message):
        all_values = worksheet.get_all_values()
        row_number = len(all_values) + 1
        column_number1 = 1  # Номер колонки, например, 2 для колонки B
        column_number2 = 2  # Номер колонки, например, 2 для колонки B
        column_number3 = 3  # Номер колонки, например, 2 для колонки B
        column_number4 = 4  # Номер колонки, например, 2 для колонки B
        column_number5 = 5  # Номер колонки, например, 2 для колонки B
        column_number6 = 6  # Номер колонки, например, 2 для колонки B
        column_number7 = 7  # Номер колонки, например, 2 для колонки B
        column_number8 = 8  # Номер колонки, например, 2 для колонки B
        column_number9 = 9  # Номер колонки, например, 2 для колонки B
        column_number10 = 10  # Номер колонки, например, 2 для колонки B
        column_number11 = 11  # Номер колонки, например, 2 для колонки B
        worksheet.update_cell(row_number, column_number1, vo1)
        worksheet.update_cell(row_number, column_number2, vo2)
        worksheet.update_cell(row_number, column_number3, vo3)
        worksheet.update_cell(row_number, column_number4, vo4)
        worksheet.update_cell(row_number, column_number5, vo5)
        worksheet.update_cell(row_number, column_number6, vo6)
        worksheet.update_cell(row_number, column_number7, vo7)
        worksheet.update_cell(row_number, column_number8, vo8)
        worksheet.update_cell(row_number, column_number9, vo9)
        worksheet.update_cell(row_number, column_number10, vo10)
        worksheet.update_cell(row_number, column_number11, username)
        await bot.send_message(id_user, 'Благодарим за заполнение анкеты, в ближайшее время с тобой свяжется @aver1413', reply_markup=kb_spec)
        await bot.send_message(CHANNEL_ID, f"""
: {vo1}
: {vo2}
: {vo3}
: {vo4}
: {vo5}
: {vo6}
: {vo7}
: {vo8}
: {vo9}
: {vo10}
: @{username}""")
    
    

