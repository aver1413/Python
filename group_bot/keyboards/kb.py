from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton("Поделиться номером телефона", request_contact=True)
keyboard.add(button)