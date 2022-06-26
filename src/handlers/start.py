import aiogram

from bot_config import bot
from .menu import check_menu, FSM


async def start(message: aiogram.types.Message):
    buttons = [['💳 Generate gift card', '💰 View available cards'],
               ['⚙️ Settings']]
    bot.add_keyboard('menu', buttons)
    await message.answer('Привет этот бот выполняет манипуляции с картами',
                         reply_markup=bot.keyboards['menu'])
    bot.add_state_handler(FSM.menu, check_menu)
    await FSM.menu.set()
