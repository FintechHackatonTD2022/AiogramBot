import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.markdown import hspoiler

from bot_config import bot
from services.draw_card.card_drawer import CardDrawer
import misc

data = {}
_ = misc.i18n.gettext


async def generate_card(message: aiogram.types.Message):
    misc.i18n.ctx_locale.set(misc.locale)
    await message.answer(_('Вы пытаетесь получить виртуальную карту'))
    await message.answer(_('Для ее получения нам необходимо узнать о вас некоторою информацию'))
    await message.answer(_('Напишите боту ваш ИИН'))
    bot.add_state_handler(FSM.get_iin, get_iin)
    await FSM.get_iin.set()


async def get_iin(message: aiogram.types.Message, state: FSMContext):
    await state.finish()  # [ ] validate
    misc.i18n.ctx_locale.set(misc.locale)
    data[f'{message.from_id}iin'] = message.text
    button = KeyboardButton(
        _('Отправить номер телефона'), request_contact=True)
    kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb.add(button)
    # [ ] save phone number
    await message.answer(_('Передайте номер телефона'), reply_markup=kb)
    await FSM.send_card.set()


class FSM(StatesGroup):
    get_iin = State()
    send_card = State()


@bot.dp.message_handler(content_types=['contact'], state=FSM.send_card)
async def send_card(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Вот твоя карта', reply_markup=ReplyKeyboardRemove())
    cvv = hspoiler('228')
    caption = f'CVV: {cvv}'
    img = CardDrawer.draw_to_input_file(
        1234567890991337, "13/37", "DOOM SLAYER")
    await message.answer_photo(img, caption=caption)
