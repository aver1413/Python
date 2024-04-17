from aiogram import types
from create_bot import dp, bot
import sqlite3 
from keyboards.kb import keyboard_admin
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdmin(StatesGroup):
    user = State()
    delete = State()
    admin1 = State()
    admin2 = State()
    del_adm1 = State()


@dp.message_handler(commands="cancel", state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Хорошо, выбери другое действие", reply_markup=keyboard_admin)

async def check_admin(id):
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ID FROM admin')
    ids = cursor.fetchall()
    conn.close()
    for id_admin in ids:
        if id in id_admin:
            return True
    return 'Ты не администратор'




@dp.message_handler(commands='admin')
async def admin(message: types.Message):
    id = message.from_user.id
    check = await check_admin(id)
    if check == True:
        await bot.send_message(id, 'Выбери действие', reply_markup=keyboard_admin)
    else:
        await bot.send_message(id, check)




@dp.message_handler(text='Просмотреть пользователя', state=None)
async def check_user(message: types.Message):
    id = message.from_user.id
    check = await check_admin(id)
    if check == True:
         await bot.send_message(id, 'Пришли username без @\nВведи /cancel если передумал')
         await FSMAdmin.user.set()
    else:
        await bot.send_message(id, 'Ты не администратор')




@dp.message_handler(state=FSMAdmin.user)
async def username(message: types.Message, state: FSMContext):
    username = message.text
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    query = "SELECT * FROM user_info WHERE username = ?"
    cursor.execute(query, (username,))
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
        photo1_path = f'Photo/{id}+car_photo.jpg'
        with open(photo1_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Фото автомобиля с ГОС номером')
        photo2_path = f'Photo/{id}+sts_front.jpg'
        with open(photo2_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Фото СТС с лицовой стороны')
        photo3_path = f'Photo/{id}+sts_back.jpg'
        with open(photo3_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Фото СТС с обратной стороны')
        photo4_path = f'Photo/{id}+driver_license_front.jpg'
        with open(photo4_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Фото ВУ с лицевой стороны')
        photo5_path = f'Photo/{id}+driver_license_back.jpg'
        with open(photo5_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Фото ВУ с обратной стороны')
        photo6_path = f'Photo/{id}+selfie_with_license.jpg'
        with open(photo6_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Селфи с ВУ')
        photo7_path = f'Photo/{id}+selfie_with_car.jpg'
        with open(photo7_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Селфи с авто')
    else:
        await message.answer("Пользователь не найден.")
    conn.close()
    await state.finish()



@dp.message_handler(text='Удалить пользователя из БД', state=None)
async def delete(message: types.Message):
    id = message.from_user.id
    check = await check_admin(id)
    if check == True:
         await bot.send_message(id, 'Пришли username без @\nВведи /cancel если передумал')
         await FSMAdmin.delete.set()
    else:
        await bot.send_message(id, 'Ты не администратор')



@dp.message_handler(state=FSMAdmin.delete)
async def delete2(message: types.Message, state: FSMContext):
    username = message.text
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    query = "DELETE FROM user_info WHERE username = ?"
    cursor.execute(query, (username,))
    conn.commit()
    if cursor.rowcount > 0:
        await message.answer(f"Пользователь с username '@{username}' удален.")
    else:
        await message.answer("Пользователь не найден.")
    conn.close()
    await state.finish()


@dp.message_handler(text='Добавить администратора', state=None)
async def add_admin(message: types.Message):
    id = message.from_user.id
    check = await check_admin(id)
    if check == True:
         await bot.send_message(id, 'Пришли username без @\nВведи /cancel если передумал')
         await FSMAdmin.admin1.set()
    else:
        await bot.send_message(id, 'Ты не администратор')



@dp.message_handler(state=FSMAdmin.admin1)
async def add_admin2(message: types.Message, state: FSMContext):
    global user
    user = message.text
    await bot.send_message(message.from_user.id, 'Теперь пришли ID администратора\nID можно получить переслав любое сообщение пользователя в бота @getmyid_bot\nВведи /cancel если передумал')
    await FSMAdmin.admin2.set()

@dp.message_handler(state=FSMAdmin.admin2)
async def add_admin3(message: types.Message, state: FSMContext):
    global userid
    userid = message.text
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    query = "INSERT INTO admin (username, ID) VALUES (?, ?)"
    cursor.execute(query, (user, userid))
    conn.commit()
    conn.close()
    await message.answer('Администратор успешно добавлен в базу данных.')
    await state.finish()



@dp.message_handler(text='Удалить администратора', state=None)
async def del_admin(message: types.Message):
    id = message.from_user.id
    check = await check_admin(id)
    if check == True:
         await bot.send_message(id, 'Пришли username без @\nВведи /cancel если передумал')
         await FSMAdmin.del_adm1.set()
    else:
        await bot.send_message(id, 'Ты не администратор')



@dp.message_handler(state=FSMAdmin.del_adm1)
async def del_admin2(message: types.Message, state: FSMContext):
    global user
    user = message.text
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    query = "DELETE FROM admin WHERE username = ?"
    cursor.execute(query, (user,))
    conn.commit() 
    if cursor.rowcount > 0:
        await message.answer(f"Администратор с username '{user}' успешно удален.")
    else:
        await message.answer("Администратор не найден.")
    conn.close()
    await state.finish()

