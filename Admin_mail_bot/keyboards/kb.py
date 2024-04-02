from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Орёл прилетел')
b2 = KeyboardButton('Орёл улетел')

kb = ReplyKeyboardMarkup(resize_keyboard=True)

kb.add(b1).add(b2)