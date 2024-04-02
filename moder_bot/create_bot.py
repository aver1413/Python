from aiogram import Bot
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

storage = MemoryStorage()

# bot = Bot(token=os.getenv('TOKEN'))

bot = Bot(token="")


dp = Dispatcher(bot, storage=storage)