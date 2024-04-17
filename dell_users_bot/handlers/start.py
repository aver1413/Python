
from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message



router = Router()


@router.message(CommandStart())
async def start(message: Message):
    username = message.from_user.username
    await message.answer(f'И тебе привет,{username}')






    
    

