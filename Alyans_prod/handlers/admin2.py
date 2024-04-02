from aiogram import types, Dispatcher
from create_bot import bot, dp
import sqlite3
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.func.news import send_news
from handlers.func.news_mini import send_mini_news
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import gspread
from google.auth import exceptions
from google.oauth2.service_account import Credentials


CHANNEL_ID = -100180

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardRemove


class FSMAdmin(StatesGroup):
    nick1 = State()
    nick2 = State()
    nick5 = State()
    nick6 = State()
    alldostup = State()
    dellhelper = State()
    delltrenerr = State()
    dellspec = State()
    dellstager = State()
    OUK = State()

kb_admin2 = \
InlineKeyboardMarkup (row_width=1) \
.add(InlineKeyboardButton(text='Посмотреть доступ "Стажировка"', callback_data='Посмотреть доступ "Стажировка"')) \
.add(InlineKeyboardButton(text='Посмотреть доступ "Специалист"', callback_data='Посмотреть доступ "Специалист"')) \
.add(InlineKeyboardButton(text='Cделать новость', callback_data='Cделать новость')) \
.add(InlineKeyboardButton(text='Cделать мини-новость', callback_data='Cделать мини-новость')) \
.add(InlineKeyboardButton(text='Посмотреть доступ "Helper"', callback_data='Посмотреть доступ "Helper"')) \
.add(InlineKeyboardButton(text='Посмотреть доступ "Тренер"', callback_data='Посмотреть доступ "Тренер"')) \
.add(InlineKeyboardButton(text='Выдать доступ "Helper"', callback_data='Выдать доступ "Helper"')) \
.add(InlineKeyboardButton(text='Выдать доступ "Специалист"', callback_data='Выдать доступ "Специалист"')) \
.add(InlineKeyboardButton(text='Выдать доступ "Стажёр"', callback_data='Выдать доступ "Стажёр"')) \
.add(InlineKeyboardButton(text='ID аккаунтов', callback_data='ID аккаунтов')) \
.add(InlineKeyboardButton(text='Забрать все доступы', callback_data='Забрать все доступы')) \
.add(InlineKeyboardButton(text='Забрать доступ "Стажёр"', callback_data='Забрать доступ "Стажёр"')) \
.add(InlineKeyboardButton(text='Забрать доступ "Специалист"', callback_data='Забрать доступ "Специалист"')) \
.add(InlineKeyboardButton(text='Забрать доступ "Тренер"', callback_data='Забрать доступ "Тренер"')) \
.add(InlineKeyboardButton(text='Забрать доступ "Helper"', callback_data='Забрать доступ "Helper"')) \
.add(InlineKeyboardButton(text='Посмотреть ОУК', callback_data='Посмотреть ОУК'))


@dp.callback_query_handler(text='Посмотреть доступ "Стажировка"')
async def checkstager(callback : types.CallbackQuery):
    await callback.answer()
    await perdayoverstager(callback)


@dp.callback_query_handler(text='Посмотреть доступ "Специалист"')
async def checkstager(callback : types.CallbackQuery):
    await callback.answer()
    await perdayoverspec(callback)

@dp.callback_query_handler(text='Cделать новость')
async def checkstager(callback : types.CallbackQuery):
    await callback.answer()
    await sendnewsbot(callback)


@dp.callback_query_handler(text='Cделать мини-новость')
async def checkstager(callback : types.CallbackQuery):
    await callback.answer()
    await mini_news(callback)


@dp.message_handler(commands='адм')
async def start_admin_admin(message : types.Message):
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await start_admin(message)
    else:
        await bot.send_message(message.from_user.id, 'У тебя нет доступа к админке бота')


async def start_admin(message : types.Message):
    await bot.send_message(message.from_user.id, 'Меню администратора', reply_markup=kb_admin2)



async def perdayoverstager(message: types.Message):
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:

        base = sqlite3.connect('main.db')
        cur = base.cursor()
        cur.execute('SELECT login FROM stager')
        rows = cur.fetchall()
        username_stager = [f"@{row[0]}" for row in rows]
        spisok = "\n\n".join(username_stager)

        await bot.send_message(message.from_user.id, f'Список аккаунтов с доступом "Стажировка":\n\n{spisok}')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")

async def perdayoverspec(message: types.Message):
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:

        base = sqlite3.connect('main.db')
        cur = base.cursor()
        cur.execute('SELECT USERNAME FROM spec')
        rows = cur.fetchall()
        username_spec1 = [f"@{row[0]}" for row in rows]
        spisok1 = "\n\n".join(username_spec1)
        base.close()
        await bot.send_message(message.from_user.id, f'Список аккаунтов с доступом "Специалист":\n\n{spisok1}')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")

async def sendnewsbot(message: types.Message):
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await send_news(message, State)
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")

async def mini_news(message: types.Message):
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await send_mini_news(message)
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")



@dp.message_handler(text='Посмотреть доступ "Helper"')
async def dost_helper(message: types.Message):
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:

        base = sqlite3.connect('main.db')
        cur = base.cursor()
        cur.execute('SELECT USERNAME FROM helper')
        rows = cur.fetchall()
        username_helper = [f"@{row[0]}" for row in rows]
        spisok1 = "\n\n".join(username_helper)
        base.close()
        await bot.send_message(message.from_user.id, f'Список аккаунтов с доступом "Helper":\n\n{spisok1}')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")



@dp.message_handler(text='Посмотреть доступ "Тренер"')
async def dost_trener(message: types.Message):
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:

        base = sqlite3.connect('main.db')
        cur = base.cursor()
        cur.execute('SELECT USERNAME FROM trener')
        rows = cur.fetchall()
        username_trener = [f"@{row[0]}" for row in rows]
        spisok1 = "\n\n".join(username_trener)
        base.close()
        await bot.send_message(message.from_user.id, f'Список аккаунтов с доступом "Тренер":\n\n{spisok1}')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")





@dp.message_handler(text='Выдать доступ "Тренер"', state=None)
async def dost_trener(message: types.Message):
    await FSMAdmin.nick1.set()
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await bot.send_message(message.from_user.id, f'Введи ник никнейм без @.\nПример: AVER1413')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")


@dp.message_handler(state=FSMAdmin.nick1)
async def load_nick2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nick'] = message.text
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('INSERT OR IGNORE INTO trener (USERNAME) VALUES (?)', (f"{message.text}",))
    base.commit()
    await bot.send_message(message.from_user.id, f'@{message.text} добавлен')
    await state.finish()





@dp.message_handler(text='Выдать доступ "Helper"', state=None)
async def dost_helper(message: types.Message):
    await FSMAdmin.nick2.set()
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await bot.send_message(message.from_user.id, f'Введи ник никнейм без @.\nПример: AVER1413')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")


@dp.message_handler(state=FSMAdmin.nick2)
async def load_nick3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nick'] = message.text
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('INSERT OR IGNORE INTO helper (USERNAME) VALUES (?)', (f"{message.text}",))
    base.commit()
    await bot.send_message(message.from_user.id, f'@{message.text} добавлен')
    await state.finish()



@dp.message_handler(text='Выдать доступ "Специалист"', state=None)
async def dost_spec(message: types.Message):
    await FSMAdmin.nick5.set()
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await bot.send_message(message.from_user.id, f'Введи ник никнейм без @.\nПример: AVER1413')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")


@dp.message_handler(state=FSMAdmin.nick5)
async def load_nick4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nick'] = message.text
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('INSERT OR IGNORE INTO spec (USERNAME) VALUES (?)', (f"{message.text}",))
    base.commit()
    await bot.send_message(message.from_user.id, f'@{message.text} добавлен')
    await state.finish()




@dp.message_handler(text='Выдать доступ "Стажёр"', state=None)
async def dost_stager(message: types.Message):
    await FSMAdmin.nick6.set()
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await bot.send_message(message.from_user.id, f'Введи ник никнейм без @.\nПример: AVER1413')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")


@dp.message_handler(state=FSMAdmin.nick6)
async def load_nick5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nick'] = message.text
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('INSERT OR IGNORE INTO stager (login) VALUES (?)', (f"{message.text}",))
    base.commit()
    await bot.send_message(message.from_user.id, f'@{message.text} добавлен')
    await state.finish()




@dp.message_handler(text='ID аккаунтов')
async def dost_trener(message: types.Message):
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:

        base = sqlite3.connect('main.db')
        cur = base.cursor()
        cur.execute('SELECT USERNAME FROM ID')
        rows = cur.fetchall()
        username_ID = [f"@{row[0]}" for row in rows]
        spisok1 = "\n\n".join(username_ID)
        base.close()
        await bot.send_message(message.from_user.id, f'Список аккаунтов с ID:\n\n{spisok1}')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")



@dp.message_handler(text='Забрать все доступы', state=None)
async def dell_specs(message: types.Message):
    await FSMAdmin.alldostup.set()
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await bot.send_message(message.from_user.id, f'Введи ник никнейм без @.\nПример: AVER1413')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")


@dp.message_handler(state=FSMAdmin.alldostup)
async def load_nick8(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nick'] = message.text
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('DELETE FROM spec WHERE USERNAME == ?', (f"{message.text}",))
    cur.execute('DELETE FROM helper WHERE USERNAME == ?', (f"{message.text}",))
    cur.execute('DELETE FROM trener WHERE USERNAME == ?', (f"{message.text}",))
    cur.execute('DELETE FROM stager WHERE login == ?', (f"{message.text}",))
    cur.execute('DELETE FROM ID WHERE USERNAME == ?', (f"{message.text}",))
    base.commit()
    await bot.send_message(message.from_user.id, f'@{message.text} удалён из бота целиком')
    await state.finish()



@dp.message_handler(text='Забрать доступ "Helper"', state=None)
async def dell_helper(message: types.Message):
    await FSMAdmin.dellhelper.set()
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await bot.send_message(message.from_user.id, f'Введи ник никнейм без @.\nПример: AVER1413')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")


@dp.message_handler(state=FSMAdmin.dellhelper)
async def load_nick115(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nick'] = message.text
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('DELETE FROM helper WHERE USERNAME == ?', (f"{message.text}",))
    base.commit()
    await bot.send_message(message.from_user.id, f'@{message.text} убрали доступ "Helper" этому аккаунту')
    await state.finish()




@dp.message_handler(text='Забрать доступ "Тренер"', state=None)
async def dell_trener(message: types.Message):
    await FSMAdmin.delltrenerr.set()
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await bot.send_message(message.from_user.id, f'Введи ник никнейм без @.\nПример: AVER1413')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")


@dp.message_handler(state=FSMAdmin.delltrenerr)
async def load_nick111(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nick'] = message.text
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('DELETE FROM trener WHERE USERNAME == ?', (f"{message.text}",))
    base.commit()
    await bot.send_message(message.from_user.id, f'@{message.text} убрали доступ "Тренер" этому аккаунту')
    await state.finish()



@dp.message_handler(text='Забрать доступ "Специалист"', state=None)
async def dell_spec(message: types.Message):
    await FSMAdmin.dellspec.set()
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await bot.send_message(message.from_user.id, f'Введи ник никнейм без @.\nПример: AVER1413')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")


@dp.message_handler(state=FSMAdmin.dellspec)
async def load_nick112(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nick'] = message.text
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('DELETE FROM spec WHERE USERNAME == ?', (f"{message.text}",))
    base.commit()
    await bot.send_message(message.from_user.id, f'@{message.text} убрали доступ "Тренер" этому аккаунту')
    await state.finish()



@dp.message_handler(text='Забрать доступ "Стажёр"', state=None)
async def dell_stager(message: types.Message):
    await FSMAdmin.dellstager.set()
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await bot.send_message(message.from_user.id, f'Введи ник никнейм без @.\nПример: AVER1413')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")


@dp.message_handler(state=FSMAdmin.dellstager)
async def load_nick112(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nick'] = message.text
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('DELETE FROM stager WHERE login == ?', (f"{message.text}",))
    base.commit()
    await bot.send_message(message.from_user.id, f'@{message.text} убрали доступ "Тренер" этому аккаунту')
    await state.finish()





# Указываем данные вашего Google аккаунта и ключ сервисного аккаунта
credentials = Credentials.from_service_account_file('hermal-pattern-394314-c98e9373fa4c.json', scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.Client(auth=credentials)

# Указываем ID таблицы, в которой вы хотите искать текст
spreadsheet_id = ''



@dp.message_handler(text='Посмотреть ОУК', state=None)
async def dost_trener(message: types.Message):
    await FSMAdmin.OUK.set()
    await message.delete()
    base = sqlite3.connect('main.db')
    cur = base.cursor()
    cur.execute('SELECT USERNAME FROM admin')
    rows = cur.fetchall()
    username_admin = [row[0] for row in rows]
    if message.from_user.username in username_admin:
        await bot.send_message(message.from_user.id, f'Введи фамилию и имя специалиста')
    else:
        await bot.send_message(message.from_user.id, "Увы, у тебя нет доступа к этой функции")


@dp.message_handler(state=FSMAdmin.OUK)
async def check_ouk(message: types.Message, state: FSMContext):

    search_text = message.text
    global ids
    ids = message.from_user.id
    await message.delete()
    wait = await bot.send_message(ids, 'Ожидай ~ 2 секунды')

    try:
        # Открываем нужный лист в Google таблице
        sheet = client.open_by_key(spreadsheet_id).worksheet('ОУК-Сентябрь-2023')

        # Ищем все строки, содержащие введенный текст
        search_results = sheet.findall(search_text)

        # Проверяем, были ли найдены результаты
        if search_results:
            # Создаем пустой список для хранения найденных строк
            rows_with_text = []

            # Получаем содержимое каждой найденной строки
            for result in search_results:
                row = sheet.row_values(result.row)
                name = row[1]
                udal = row[2]
                OUK1 = row[3]
                SA1 = row[4]
                OUK2 = row[5]
                SA2 = row[6]
                OUK3 = row[7]
                SA3 = row[8]
                OUK4 = row[9]
                SA4 = row[10]
                OUK5 = row[11]
                SA5 = row[12]
                OUKITOG = row[13]
                SAITOG = row[14]
                rows_with_text.append(row)

            # Отправляем результаты пользователю
            response = '\n'.join([' | '.join(row) for row in rows_with_text])
            # await message.answer(response)
            await bot.send_message(message.from_user.id, f"""<i>Специалист:</i> <b>{name}</b>
""", parse_mode='HTML', reply_markup=kb_admin2)
            await bot.delete_message(chat_id=ids, message_id=wait.message_id)
        else:
            await message.answer('Текст не найден')
            await message.answer(f"Поиск по - {search_text}")

    except exceptions.GoogleAuthError as e:
        await message.answer('Произошла ошибка аутентификации Google: ' + str(e))
    except gspread.SpreadsheetNotFound:
        await message.answer('Таблица не найдена')

    await state.finish()





    