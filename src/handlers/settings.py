import aiogram

import misc
from misc import i18n

_ = i18n.gettext


async def set_locale_en(message: aiogram.types.Message):
    misc.locale = 'en'


async def set_locale_ru(message: aiogram.types.Message):
    misc.locale = 'ru'


async def set_locale_kaz(message: aiogram.types.Message):
    misc.locale = 'kaz'
