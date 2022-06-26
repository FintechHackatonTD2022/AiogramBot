import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.markdown import hspoiler
import misc
from bot_config import bot
from utils.localization import set_locale

_ = misc.i18n.gettext


async def init(message: aiogram.types.Message):
    buttons = [['Сменить язык']]
    bot.add_keyboard('settings_menu', buttons)
    await message.answer('Что вы хотите изменить',
                         reply_markup=bot.keyboards['settings_menu'])
    bot.add_state_handler(FSM.settings_menu, settings_menu)
    await FSM.settings_menu.set()


async def settings_menu(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    match message.text:
        case 'Сменить язык':
            buttons = [['🇷🇺', '🇰🇿', '🏴󠁧󠁢󠁥󠁮󠁧󠁿']]
            bot.add_keyboard('locales', buttons)
            await message.answer('Выберите язык',
                                 reply_markup=bot.keyboards['locales'])
            bot.add_state_handler(FSM.locales_menu, locales_menu)
            await FSM.locales_menu.set()


async def locales_menu(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    match message.text:
        case '🇷🇺':
            await set_locale('ru')
        case '🇰🇿':
            await set_locale('kaz')
        case '🏴󠁧󠁢󠁥󠁮󠁧󠁿':
            await set_locale('en')


class FSM(StatesGroup):
    settings_menu = State()
    locales_menu = State()
