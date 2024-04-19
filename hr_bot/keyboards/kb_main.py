from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Адаптация')
b2 = KeyboardButton('КР')
b3 = KeyboardButton('Выгорание')
b4 = KeyboardButton('Аналитика')
b5 = KeyboardButton('ЭИ')

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(b1).insert(b2).add(b3).insert(b4).add(b5)

