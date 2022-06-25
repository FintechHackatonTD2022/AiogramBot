import aiogram

from bot_config import bot
from . import users
from . import menu


async def list_of_commands(message: aiogram.types.Message):
    text = 'Привет вот список команд которые есть в боте:\n\n'
    for cmd in users:
        text += '/%s\n' % cmd
    await message.answer(text, reply_markup=bot.keyboards['menu'])
    await menu.FSM.menu.set()
