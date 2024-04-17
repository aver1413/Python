from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton("Поделиться номером телефона", request_contact=True)
keyboard.add(button)



keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton("Просмотреть пользователя")
button2 = KeyboardButton("Удалить пользователя из БД")
button3 = KeyboardButton("Добавить администратора")
button4 = KeyboardButton("Удалить администратора")
keyboard_admin.add(button).add(button2).add(button3).add(button4)