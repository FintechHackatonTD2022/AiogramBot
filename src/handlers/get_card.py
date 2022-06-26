import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.markdown import hspoiler

from bot_config import bot
import misc
from services.card_api import CardApi
from services.card_drawer import CardDrawer
from . import menu

_ = misc.i18n.gettext
data = {}


async def get_card(message: aiogram.types.Message):
    misc.i18n.ctx_locale.set(misc.get_locale(message.from_id))
    text = _('Вы пытаетесь восстановить виртуальную карту. ')
    text += _('Для ее получения нам необходимо узнать о вас\
         некоторую информацию: ')
    text += _('<b>Ваш ИИН: </b>')
    await message.answer(text)
    bot.add_state_handler(FSM.get_iin, get_iin)
    await FSM.get_iin.set()


async def get_iin(message: aiogram.types.Message, state: FSMContext):
    misc.i18n.ctx_locale.set(misc.get_locale(message.from_id))
    await state.finish()  # [ ] validate
    data[f'{message.from_id}iin'] = message.text
    button = KeyboardButton(
        _('Отправить номер телефона'), request_contact=True)
    kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb.add(button)
    await message.answer(_('Ваш номер телефона: '), reply_markup=kb)
    await FSM.get_contact_.set()


class FSM(StatesGroup):
    get_iin = State()
    get_contact_ = State()


@bot.dp.message_handler(content_types=['contact'], state=FSM.get_contact_)
async def get_phone_(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    data[f'{message.from_id}phone'] = message.contact.phone_number
    await send_card(message)


async def send_card(message: aiogram.types.Message):
    misc.i18n.ctx_locale.set(misc.get_locale(message.from_id))
    mes_try_create_card = await bot.send_message(
        message.from_id,
        _('Пытаемся найти карту...'))

    phone_number = data[f'{message.from_id}phone']
    iin = data[f'{message.from_id}iin']

    card_data = CardApi.get_card(phone_number, iin)
    await mes_try_create_card.edit_text(_('Карта найдена, отправляем...'))
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
