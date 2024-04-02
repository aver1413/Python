# myapp/tasks.py
from celery import Celery, shared_task
from datetime import datetime
from aiogram import Bot
from asgiref.sync import async_to_sync

# Создаем экземпляр Celery
celery = Celery('myapp')

# Настраиваем Celery
celery.config_from_object('django.conf:settings', namespace='CELERY')

# Создаем бота
bot_token = ''
channel_id = -100
bot = Bot(token=bot_token)

# Задача с использованием async_to_sync
@shared_task
def send_greetings():
    # Преобразуем асинхронную функцию в синхронную
    async_to_sync(bot.send_message)(chat_id=channel_id, text='test')
    print("привет", datetime.now())
