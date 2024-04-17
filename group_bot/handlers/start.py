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
Для того, чтобы перейти в группы - тебе необходимо заполнить анкету
Начнем с предоставления номера
Чтобы предоставить свой номер - нажми на кнопку ниже 👇
                           """, reply_markup=keyboard)



@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=None)
async def handle_contact(message: types.Message):
    global phone_number, id, fullname, username ## номер телефона
    contact = message.contact 
    id = message.from_user.id # ИД тг
    fullname = message.from_user.full_name ## Полное имя
    username = message.from_user.username ## Юзернейм тг
    phone_number = contact.phone_number
    base = sqlite3.connect('user_info.db')
    cur = base.cursor()
    cur.execute('SELECT ID FROM user_info')
    check1 = [row[0] for row in cur.fetchall()]
    if message.from_user.id in check1:
        await bot.send_message(message.from_user.id, 'Упс...\nТвоя анкета уже заполнена 👌')
    else:
        await bot.send_message(id, 'Напиши своё ФИО\nДля того, чтобы прервать заполнение анкеты - веди /cancel')
        await FSMAdmin.name.set()


    
@dp.message_handler(state=FSMAdmin.name)
async def v1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global name
        name = message.text
    await FSMAdmin.next()
    await bot.send_message(id, 'Теперь введи свой город 🏙')



@dp.message_handler(state=FSMAdmin.city)
async def v2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global city
        city = message.text
    await FSMAdmin.next()
    await bot.send_message(id, 'Теперь введи свою марку автомобиля 🚘')


@dp.message_handler(state=FSMAdmin.car_make)
async def v3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global car_make
        car_make = message.text
    await FSMAdmin.next()
    await bot.send_message(id, 'Теперь введи модель своего автомобиля 🚘')


@dp.message_handler(state=FSMAdmin.car_model)
async def v4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global car_model
        car_model = message.text
    await FSMAdmin.next()
    await bot.send_message(id, 'Теперь пришли ГОС номер своего автомобиля 🚔')


@dp.message_handler(state=FSMAdmin.license_plate)
async def v5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        global license_plate
        license_plate = message.text
    await FSMAdmin.next()
    await bot.send_message(id, 'Теперь пришли фото автомобиля где будет виден ГОС номер 🚔')


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
    await FSMAdmin.next()
    await message.reply('Теперь пришли фото СТС с лицевой стороны 📑')


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
    await FSMAdmin.next()
    await message.reply('Теперь пришли фото СТС с обратной стороны стороны 📑')


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
    await FSMAdmin.next()
    await message.reply('Теперь пришли фото ВУ с лицевой стороны 📑')


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
    await FSMAdmin.next()
    await message.reply('Теперь пришли фото ВУ с обратной стороны стороны 📑')


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
    await FSMAdmin.next()
    await message.reply('Теперь пришли селфи с ВУ 📑')


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
    await FSMAdmin.next()
    await message.reply('Теперь пришли селфи с автомобилем, чтобы был виден ГОС номер 📑')


@dp.message_handler(content_types=['photo'], state=FSMAdmin.selfie_with_car)
async def v9(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        file_id = message.photo[-1].file_id
        photo = await bot.download_file_by_id(file_id)
        folder_path = 'Photo'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        global selfie_with_car, check_done
        check_done = 0
        selfie_with_car = f"{message.from_user.id}+selfie_with_car.jpg"
        filepath = os.path.join(folder_path, selfie_with_car)
        with open(filepath, 'wb') as new_file:
            new_file.write(photo.read())
    await state.finish()
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO user_info (ID, name, username, fullname, phone_number, city, car_make, car_model, license_plate,
                            car_photo, sts_front, sts_back, driver_license_front, driver_license_back, selfie_with_license,
                            selfie_with_car, check_done)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, name, username, fullname, phone_number, city, car_make, car_model, license_plate, car_photo,
            sts_front, sts_back, driver_license_front, driver_license_back, selfie_with_license, selfie_with_car, check_done))
    conn.commit()
    conn.close()
    await bot.send_message(message.from_user.id, text1)
    sleep(1)
    await bot.send_message(message.from_user.id, text2)
    base = sqlite3.connect('user_info.db')
    cur = base.cursor()
    cur.execute('SELECT ID FROM admin')
    ids = cur.fetchall()
    base.close()
    for id_admin in ids:
        await bot.send_message(id_admin[0], f"""
Новая анкета:
ID: {id}
ФИО: {name}
username TG: @{username}
Полное имя TG: {fullname}
Номер телефона: {phone_number}
Город: {city}
Марка машины: {car_make}
Модель машины: {car_model}
ГОС номер: {license_plate}
""")
        photo1_path = f'Photo/{id}+car_photo.jpg'
        with open(photo1_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=id_admin[0], photo=photo_file, caption='Фото автомобиля с ГОС номером')
        photo2_path = f'Photo/{id}+sts_front.jpg'
        with open(photo2_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=id_admin[0], photo=photo_file, caption='Фото СТС с лицовой стороны')
        photo3_path = f'Photo/{id}+sts_back.jpg'
        with open(photo3_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=id_admin[0], photo=photo_file, caption='Фото СТС с обратной стороны')
        photo4_path = f'Photo/{id}+driver_license_front.jpg'
        with open(photo4_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=id_admin[0], photo=photo_file, caption='Фото ВУ с лицевой стороны')
        photo5_path = f'Photo/{id}+driver_license_back.jpg'
        with open(photo5_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=id_admin[0], photo=photo_file, caption='Фото ВУ с обратной стороны')
        photo6_path = f'Photo/{id}+selfie_with_license.jpg'
        with open(photo6_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=id_admin[0], photo=photo_file, caption='Селфи с ВУ')
        photo7_path = f'Photo/{id}+selfie_with_car.jpg'
        with open(photo7_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=id_admin[0], photo=photo_file, caption='Селфи с авто')



