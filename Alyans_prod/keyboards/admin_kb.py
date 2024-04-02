from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('Посмотреть доступ "Стажировка"')
b2 = KeyboardButton('Посмотреть доступ "Специалист"')
b3 = KeyboardButton('Cделать новость')
b4 = KeyboardButton('Cделать мини-новость')
b5 = KeyboardButton('Посмотреть доступ "Helper"')
b6 = KeyboardButton('Посмотреть доступ "Тренер"')
b7 = KeyboardButton('Выдать доступ "Тренер"')
b8 = KeyboardButton('Выдать доступ "Helper"')
b9 = KeyboardButton('Выдать доступ "Специалист"')
b10 = KeyboardButton('Выдать доступ "Стажёр"')
b12 = KeyboardButton('ID аккаунтов')
b13 = KeyboardButton('Забрать все доступы')
b14 = KeyboardButton('Забрать доступ "Стажёр"')
b15 = KeyboardButton('Забрать доступ "Специалист"')
b16 = KeyboardButton('Забрать доступ "Тренер"')
b17 = KeyboardButton('Забрать доступ "Helper"')
b18 = KeyboardButton('Меню спеца')
b19 = KeyboardButton('Посмотреть ОУК')
b20 = KeyboardButton('Сделать мини-новость(фото)')



kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(b3).add(b4).add(b20).add(b19).add(b10).add(b9).add(b8).add(b7).add(b1).add(b2).add(b5).add(b6).add(b12).add(b13).add(b14).add(b15).add(b16).add(b17).add(b18)