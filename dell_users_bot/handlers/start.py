
from aiogram import F, Router, Bot
from aiogram.filters.command import Command
from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message
from token_bot import TOKEN
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

router = Router()
bot = Bot(token=TOKEN)

button = KeyboardButton(text="Поделиться номером телефона", request_contact=True)

# Добавляем кнопку на клавиатуру
markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button)

async def check_whitelist(username):
    with open('whitelist.txt', 'r') as f:
        whitelist = f.read()
        print(whitelist)
        if username in whitelist:
            return(True)
        else:
            return(False)




@router.message(CommandStart())
async def start(message: Message):
    username = message.from_user.username
    fullname = message.from_user.full_name
    await bot.send_message(message.from_user.id, f'{fullname}, добро пожаловать в бота 😎')
    check = await check_whitelist(username)
    if check == True:
        await bot.send_message(message.from_user.id, 'Инструкция по боту:', reply_markup=markup)
    else:
        await bot.send_message(message.from_user.id, 'У тебя нет доступа к боту 😔')




@router.message(F.CONTACT)
async def contact_handler(message: Message):
    phone_number = message.contact.phone_number
    await bot.send_message(message.chat.id, "Благодарю! Твой номер телефона сохранен.")
    
    

