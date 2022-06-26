import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import misc
from bot_config import bot
from .cards import generate_card
from .get_card import get_card
from .settings import init


async def check_menu(message: aiogram.types.Message, state: FSMContext):
    misc.i18n.ctx_locale.set(misc.get_locale(message.from_id))
    await state.finish()
    match message.text:
        case '💳 Открыть предоплаченную карту':
            await generate_card(message)
        case '💰 Восстановить карту':
            await get_card(message)
        case '⚙️ Настройки':
            await init(message)


class FSM(StatesGroup):
    menu = State()
