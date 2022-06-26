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
from services.validator import Validator

data = {}
_ = misc.i18n.gettext


async def generate_card(message: aiogram.types.Message):
    misc.i18n.ctx_locale.set(misc.get_locale(message.from_id))
    text = _('Вы пытаетесь получить виртуальную карту.')
    text += _('Для её получения нам необходимо узнать о вас\
         некоторую информацию, это не займет много времени:\n')
    text += _('<b>Ваш ИИН:</b>')
    await message.answer(text)
    bot.add_state_handler(FSM.get_iin, get_iin)
    await FSM.get_iin.set()


async def get_iin(message: aiogram.types.Message, state: FSMContext):
    misc.i18n.ctx_locale.set(misc.get_locale(message.from_id))
    await state.finish()  # [ ] validate
    misc.i18n.ctx_locale.set(misc.locale)

    if Validator.validate_iin(message.text):
        data[f'{message.from_id}iin'] = message.text
        button = KeyboardButton(
            _('Отправить номер телефона'), request_contact=True)
        kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        kb.add(button)
        await message.answer(_('Ваш номер телефона:'), reply_markup=kb)
        await FSM.get_contact.set()
    else:
        await message.answer('Введите корректный ИИН')
        await FSM.get_iin.set()


class FSM(StatesGroup):
    get_iin = State()
    get_amount = State()
    get_contact = State()


@bot.dp.message_handler(content_types=['contact'], state=FSM.get_contact)
async def get_phone(message: aiogram.types.Message, state: FSMContext):
    misc.i18n.ctx_locale.set(misc.get_locale(message.from_id))
    await state.finish()
    data[f'{message.from_id}phone'] = message.contact.phone_number
    await message.answer(_('Последний вопрос: на какую сумму открыть карту?'))
    bot.add_state_handler(FSM.get_amount, get_amount)
    await FSM.get_amount.set()


async def get_amount(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    if Validator.validate_amount(message.text):
        data[f'{message.from_id}amount'] = message.text
        await send_card(message)
    else:
        await message.answer('Введите корректную сумму')
        await FSM.get_amount.set()


async def send_card(message: aiogram.types.Message):
    misc.i18n.ctx_locale.set(misc.get_locale(message.from_id))
    mes_try_create_card = await bot.send_message(
        message.from_id,
        _('Пытаемся создать карту...'))

    phone_number = data[f'{message.from_id}phone']
    iin = data[f'{message.from_id}iin']
    amount = data[f'{message.from_id}amount']

    card_data = CardApi.create_card(phone_number, iin, amount)
    await mes_try_create_card.edit_text(_('Карта одобрена, отправляем...'))
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
