from aiogram import types
from create_bot import dp, bot
from keyboards.kb import keyboard
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3
import os
from handlers.text import text1, text2
from time import sleep



class FSMAdmin(StatesGroup):
    name = State()
    city = State()
    car_make = State()
    car_model = State()
    license_plate = State()
    car_photo = State()
    sts_front = State()
    sts_back = State()
    sts_back = State()
    driver_license_front = State()
    driver_license_back = State()
    selfie_with_license = State()
    selfie_with_car = State()


@dp.message_handler(commands="cancel", state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Заполнение анкеты остановлено, чтобы заполнить её заново - введи /start", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, """
Добро пожаловать в бота 😎
Для того, чтобы перейти в группы - вам необходимо заполнить анкету
Начнем с предоставления номера
Чтобы предоставить свой номер - нажмите на кнопку ниже 👇
                           """, reply_markup=keyboard)
    id = message.from_user.id
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_info (id) VALUES (?)", (id,))
    conn.commit()
    conn.close()




@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=None)
async def handle_contact(message: types.Message):
    global phone_number, id, fullname, username ## номер телефона
    contact = message.contact # ИД тг
    phone_number = contact.phone_number
    id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET phone_number = ? WHERE id = ?", (phone_number, id))
    conn.commit()
    conn.close()
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET username = ? WHERE id = ?", (username, id))
    conn.commit()
    conn.close()
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET fullname = ? WHERE id = ?", (fullname, id))
    conn.commit()
    conn.close()
    await message.reply('Напишите своё ФИО\nДля того, чтобы прервать заполнение анкеты - ведите /cancel')
    await FSMAdmin.next()


    
@dp.message_handler(state=FSMAdmin.name)
async def v1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global name
        name = message.text
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET name = ? WHERE id = ?", (name, id))
        conn.commit()
        conn.close()
    await message.reply('Теперь введите свой город 🏙')
    await FSMAdmin.next()



@dp.message_handler(state=FSMAdmin.city)
async def v2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global city
        city = message.text
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET city = ? WHERE id = ?", (city, id))
        conn.commit()
        conn.close()
    await message.reply('Теперь введите свою марку автомобиля 🚘')
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.car_make)
async def v3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global car_make
        car_make = message.text
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET car_make = ? WHERE id = ?", (car_make, id))
        conn.commit()
        conn.close()
    await message.reply('Теперь введите модель своего автомобиля 🚘')
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.car_model)
async def v4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global car_model
        car_model = message.text
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET car_model = ? WHERE id = ?", (car_model, id))
        conn.commit()
        conn.close()
    await message.reply('Теперь пришлите ГОС номер своего автомобиля 🚔')
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.license_plate)
async def v5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global license_plate
        license_plate = message.text
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET license_plate = ? WHERE id = ?", (license_plate, id))
        conn.commit()
        conn.close()
    await message.reply('Теперь пришлите фото автомобиля где будет виден ГОС номер 🚔\nФотографию нужно прислать с сжатием.')
    await FSMAdmin.next()


@dp.message_handler(content_types=['photo'], state=FSMAdmin.car_photo)
async def v6(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        file_id = message.photo[-1].file_id
        photo = await bot.download_file_by_id(file_id)
        folder_path = 'Photo'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        global car_photo
        car_photo = f"{message.from_user.id}+car_photo.jpg"
        filepath = os.path.join(folder_path, car_photo)
        with open(filepath, 'wb') as new_file:
            new_file.write(photo.read())
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET car_photo = ? WHERE id = ?", (car_photo, id))
        conn.commit()
        conn.close()
    await message.reply('Теперь пришлите фото СТС с лицевой стороны 📑\nФотографию нужно прислать с сжатием.')
    await FSMAdmin.next()


@dp.message_handler(content_types=['photo'], state=FSMAdmin.sts_front)
async def v7(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        file_id = message.photo[-1].file_id
        photo = await bot.download_file_by_id(file_id)
        folder_path = 'Photo'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        global sts_front
        sts_front = f"{message.from_user.id}+sts_front.jpg"
        filepath = os.path.join(folder_path, sts_front)
        with open(filepath, 'wb') as new_file:
            new_file.write(photo.read())
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET sts_front = ? WHERE id = ?", (sts_front, id))
        conn.commit()
        conn.close()
    await message.reply('Теперь пришлите фото СТС с обратной стороны 📑\nФотографию нужно прислать с сжатием.')
    await FSMAdmin.next()


@dp.message_handler(content_types=['photo'], state=FSMAdmin.sts_back)
async def v8(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        file_id = message.photo[-1].file_id
        photo = await bot.download_file_by_id(file_id)
        folder_path = 'Photo'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        global sts_back
        sts_back = f"{message.from_user.id}+sts_back.jpg"
        filepath = os.path.join(folder_path, sts_back)
        with open(filepath, 'wb') as new_file:
            new_file.write(photo.read())
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET sts_back = ? WHERE id = ?", (sts_back, id))
        conn.commit()
        conn.close()
    await message.reply('Теперь пришлите фото ВУ с лицевой стороны 📑\nФотографию нужно прислать с сжатием.')
    await FSMAdmin.next()

@dp.message_handler(content_types=['photo'], state=FSMAdmin.driver_license_front)
async def v9(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        file_id = message.photo[-1].file_id
        photo = await bot.download_file_by_id(file_id)
        folder_path = 'Photo'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        global driver_license_front
        driver_license_front = f"{message.from_user.id}+driver_license_front.jpg"
        filepath = os.path.join(folder_path, driver_license_front)
        with open(filepath, 'wb') as new_file:
            new_file.write(photo.read())
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET driver_license_front = ? WHERE id = ?", (driver_license_front, id))
        conn.commit()
        conn.close()
    await message.reply('Теперь пришлите фото ВУ с обратной стороны 📑\nФотографию нужно прислать с сжатием.')
    await FSMAdmin.next()


@dp.message_handler(content_types=['photo'], state=FSMAdmin.driver_license_back)
async def v9(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        file_id = message.photo[-1].file_id
        photo = await bot.download_file_by_id(file_id)
        folder_path = 'Photo'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        global driver_license_back
        driver_license_back = f"{message.from_user.id}+driver_license_back.jpg"
        filepath = os.path.join(folder_path, driver_license_back)
        with open(filepath, 'wb') as new_file:
            new_file.write(photo.read())
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET driver_license_back = ? WHERE id = ?", (driver_license_back, id))
        conn.commit()
        conn.close()
    await message.reply('Теперь пришлите селфи с ВУ 📑\nФотографию нужно прислать с сжатием.')
    await FSMAdmin.next()


@dp.message_handler(content_types=['photo'], state=FSMAdmin.selfie_with_license)
async def v9(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        file_id = message.photo[-1].file_id
        photo = await bot.download_file_by_id(file_id)
        folder_path = 'Photo'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        global selfie_with_license
        selfie_with_license = f"{message.from_user.id}+selfie_with_license.jpg"
        filepath = os.path.join(folder_path, selfie_with_license)
        with open(filepath, 'wb') as new_file:
            new_file.write(photo.read())
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET selfie_with_license = ? WHERE id = ?", (selfie_with_license, id))
        conn.commit()
        conn.close()
    await message.reply('Теперь пришлите селфи с автомобилем, чтобы был виден ГОС номер 📑\nФотографию нужно прислать с сжатием.')
    await FSMAdmin.next()


@dp.message_handler(content_types=['photo'], state=FSMAdmin.selfie_with_car)
async def v9(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        id = message.from_user.id 
        file_id = message.photo[-1].file_id
        photo = await bot.download_file_by_id(file_id)
        folder_path = 'Photo'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        global selfie_with_car
        selfie_with_car = f"{message.from_user.id}+selfie_with_car.jpg"
        filepath = os.path.join(folder_path, selfie_with_car)
        with open(filepath, 'wb') as new_file:
            new_file.write(photo.read())
        id = message.from_user.id
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET selfie_with_car = ? WHERE id = ?", (selfie_with_car, id))
        conn.commit()
        conn.close()
    await state.finish()
    await bot.send_message(message.from_user.id, text1, disable_web_page_preview=True)
    sleep(1)
    await bot.send_message(message.from_user.id, text2, disable_web_page_preview=True)
    