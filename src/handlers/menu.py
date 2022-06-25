import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_config import bot
from .cards import generate_card


async def check_menu(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    match message.text:
        case '💳 Generate gift card':
            await generate_card(message)
        case '💰 View available cards':
            await message.answer('Someday it will work',
                                 reply_markup=bot.keyboards['menu'])
            await FSM.menu.set()


class FSM(StatesGroup):
    menu = State()
