import aiogram

from bot_config import bot
from . import users
from . import menu

import misc
from misc import i18n

_ = i18n.gettext


async def list_of_commands(message: aiogram.types.Message):
    i18n.ctx_locale.set(misc.locale)
    text = _('Привет вот список команд которые есть в боте:\n\n')
    for cmd in users:
        text += '/%s\n' % cmd
    await message.answer(text, reply_markup=bot.keyboards['menu'])
    await menu.FSM.menu.set()
