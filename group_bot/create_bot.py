from aiogram import Bot
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from token_bot import TOKEN

storage = MemoryStorage()


bot = Bot(token=TOKEN)



dp = Dispatcher(bot, storage=storage)