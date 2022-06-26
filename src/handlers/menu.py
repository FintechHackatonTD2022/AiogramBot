import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from .cards import generate_card
from .settings import init


async def check_menu(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    match message.text:
        case '💳 Generate gift card':
            await generate_card(message)
        case '💰 View available cards':
            await message.answer('Someday it will work')
        case '⚙️ Settings':
            await init(message)


class FSM(StatesGroup):
    menu = State()
