from aiogram import types, Dispatcher
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


CHANNEL_ID = 377220930

class FSMAdmin(StatesGroup):
    photo = State()



# @dp.message_handler(commands='ot')
async def ot(message : types.Message):
    await FSMAdmin.photo.set()
    await message.answer("Отправь скриншот")
    await message.delete()
   



async def forward_photo(message: types.Message,  state: FSMContext):
    # Получаем информацию о фото
    photo = message.photo[-1]
    await bot.send_message(CHANNEL_ID, f"""{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} прислал ответ""")
    await bot.send_photo(CHANNEL_ID, photo=photo.file_id)
    await message.reply("Отправил твой ответ")
    await state.finish()

        

def ot_handlers(dp : Dispatcher):
    dp.register_message_handler(ot, commands='ot', state=None)
    # dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(forward_photo,content_types=types.ContentTypes.PHOTO, state=FSMAdmin.photo)