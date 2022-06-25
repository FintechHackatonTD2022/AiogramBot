from io import BytesIO
import io
import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hspoiler
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types.input_file import InputFile

from services.draw_card.draw_card import draw_card
from bot_config import bot


data = {}


async def generate_card(message: aiogram.types.Message):
    await message.answer('Вы пытаетесь получить виртуальную карту')
    await message.answer('Для ее получения нам необходимо узнать о вас некоторою информацию')
    await message.answer('Напишите боту ваш ИИН')
    bot.add_state_handler(FSM.get_iin, get_iin)
    await FSM.get_iin.set()


async def get_iin(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    data[f'{message.from_id}iin'] = message.text
    button = KeyboardButton('Отправить номер телефона', request_contact=True)
    kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb.add(button)
    # [ ] save phone number
    await message.answer('Передайте номер телефона', reply_markup=kb)
    await FSM.send_card.set()


class FSM(StatesGroup):
    get_iin = State()
    send_card = State()


@bot.dp.message_handler(content_types=['contact'], state=FSM.send_card)
async def send_card(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    card = draw_card(1234567890991337,
                     "13/37", "DOOM SLAYER", 228)
    await message.answer('Вот твоя карта', reply_markup=ReplyKeyboardRemove())
    card_bytes_io = BytesIO()
    card.save(card_bytes_io, format='PNG')
    card_bytes_io = BytesIO(card_bytes_io.getvalue())
    cvv = hspoiler('228')
    caption = f'CVV: {cvv}'
    img = InputFile(card_bytes_io, 'photo.png')
    await message.answer_photo(img, caption=caption)
