from aiogram import types
from create_bot import dp, bot
from keyboards.kb import keyboard
import sqlite3


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, """
Добро пожаловать в бота 😎
Для того, чтобы перейти в группы - тебе необходимо заполнить анкету
Начнем с предоставления номера
Чтобы предоставить свой номер - нажми на кнопку ниже 👇
                           """, reply_markup=keyboard)

    DATABASE_FILE = 'car_info.db'
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS car_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        username TEXT,
        name TEXT,
        city TEXT,
        car_make TEXT,
        car_model TEXT,
        license_plate TEXT,
        car_photo_front TEXT,
        car_photo_back TEXT,
        sts_front TEXT,
        sts_back TEXT,
        driver_license_front TEXT,
        driver_license_back TEXT
    )
''')

# Сохранение изменений
    conn.commit()

# Закрытие соединения
    conn.close()


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def handle_contact(message: types.Message):
    contact = message.contact
    if contact:
        phone_number = contact.phone_number
        with open('number.txt', 'w') as file:
            file.write(phone_number)
        await message.answer(f"Спасибо! Ваш номер телефона {phone_number} был сохранен.")
    else:
        await message.answer("Пожалуйста, поделитесь своим номером телефона через кнопку.")
    


@dp.message_handler(content_types=types.ContentTypes.ANY, run_task=True)
async def check_user(message: types.Message):
    user_id = message.from_user.id
    chat_type = message.chat.type
    if chat_type not in ['group', 'supergroup']:
        return
    with open('ver.txt', 'r') as file:
        verified_users = file.read().splitlines()
    if str(user_id) not in verified_users:
        await message.delete()
        await message.answer(f"Вам запрещено отправлять сообщения в этой группе.")

    




