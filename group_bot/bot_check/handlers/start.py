from aiogram import types
from create_bot import dp, bot
import sqlite3
import json
from path_bd import path



@dp.message_handler(commands='start')
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Бот проверки пользователей\nПерешлите мне сообщение пользователя")

async def check_admin(id):
    conn = sqlite3.connect(f'{path}user_info.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ID FROM admin_anket')
    ids = cursor.fetchall()
    conn.close()
    for id_admin in ids:
        if id in id_admin:
            return True
    return 'Ты не администратор'

@dp.message_handler(content_types=types.ContentType.ANY, is_forwarded=True)
async def handle_forwarded_message(message: types.Message):
    print(message)
    sender_name = message.forward_sender_name
    print(sender_name)
    id = message.from_user.id
    check = await check_admin(id)
    if check == True:
        try:
            forwarded_user_id = message.forward_from.first_name
        except AttributeError:
            forwarded_user_id = sender_name
        print(forwarded_user_id)
        conn = sqlite3.connect(f'{path}user_info.db')
        cursor = conn.cursor()
        query = "SELECT * FROM user_info WHERE fullname = ?"
        cursor.execute(query, (forwarded_user_id,))
        row = cursor.fetchone() 
        if row:
            id, name, fullname, username, phone_number, city, car_make, car_model, license_plate, car_photo, sts_front, sts_back, driver_license_front, driver_license_back, selfie_with_license, selfie_with_car, check = row
            response = f'''
ID: {id}
ФИО: {name}
Полное имя TG: {username}
username TG: @{fullname}
Номер телефона: {phone_number}
Город: {city}
Марка машины: {car_make}
Модель машины: {car_model}
ГОС номер: {license_plate}
            '''
            await message.answer(response)
            photo1_path = f'{path}Photo/{id}+car_photo.jpg'
            with open(photo1_path, 'rb') as photo_file:
                await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Фото автомобиля с ГОС номером')
            photo2_path = f'{path}Photo/{id}+sts_front.jpg'
            with open(photo2_path, 'rb') as photo_file:
                await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Фото СТС с лицовой стороны')
            photo3_path = f'{path}Photo/{id}+sts_back.jpg'
            with open(photo3_path, 'rb') as photo_file:
                await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Фото СТС с обратной стороны')
            photo4_path = f'{path}Photo/{id}+driver_license_front.jpg'
            with open(photo4_path, 'rb') as photo_file:
                await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Фото ВУ с лицевой стороны')
            photo5_path = f'{path}Photo/{id}+driver_license_back.jpg'
            with open(photo5_path, 'rb') as photo_file:
                await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Фото ВУ с обратной стороны')
            photo6_path = f'{path}Photo/{id}+selfie_with_license.jpg'
            with open(photo6_path, 'rb') as photo_file:
                await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Селфи с ВУ')
            photo7_path = f'{path}Photo/{id}+selfie_with_car.jpg'
            with open(photo7_path, 'rb') as photo_file:
                await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Селфи с авто')
        else:
            await message.answer("Пользователь не найден.")
    else:
        await bot.send_message(id, check)
