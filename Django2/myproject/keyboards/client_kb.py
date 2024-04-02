from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('Причины за последние 5 минут')
b2 = KeyboardButton('Общая статистика за день')
b3 = KeyboardButton('Статистика за текущий месяц')
b4 = KeyboardButton('Статистика за произвольный пероид')
b5 = KeyboardButton('Выгрузить отчёт в EXCEL')
b6 = KeyboardButton('Проверить специалиста')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).add(b3).insert(b4).insert(b5).insert(b6)