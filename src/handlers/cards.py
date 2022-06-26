import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.markdown import hspoiler

import misc
from bot_config import bot
from services.card_api import CardApi
from services.card_drawer import CardDrawer
from . import menu

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
    await message.answer(_('Передайте номер телефона'), reply_markup=kb)
    await FSM.send_card.set()


class FSM(StatesGroup):
    get_iin = State()
    get_amount = State()
    send_card = State()


@bot.dp.message_handler(content_types=['contact'], state=FSM.send_card)
async def send_card(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    data[f'{message.from_id}phone'] = message.contact.phone_number
    await message.answer('И последний вопрос на какую сумму открыть карту?')
    bot.add_state_handler(FSM.get_amount, get_amount)
    await FSM.get_amount.set()


async def get_amount(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    data[f'{message.from_id}amount'] = message.text

    mes_try_create_card = await bot.send_message(
        message.from_id,
        'Пытаемся сделать карту...',)

    phone_number = data[f'{message.from_id}phone']
    iin = data[f'{message.from_id}iin']
    amount = data[f'{message.from_id}amount']

    card_data = CardApi.create_card(phone_number, iin, amount)
    await mes_try_create_card.edit_text('Карта одобрена отправляем...')
    await message.answer_chat_action('upload_photo')

    img = CardDrawer.draw_to_input_file(
        int(card_data['pan']),
        f'{card_data["exp_month"]}/{card_data["exp_year"]}',
        message.from_user.full_name)

    cvv = hspoiler(card_data["cvc2"])
    caption = f'CVV: {cvv}'

    await message.answer_photo(img, caption=caption,
                               reply_markup=bot.keyboards['menu'])
    await mes_try_create_card.delete()

    await menu.FSM.menu.set()


async def get_card(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
