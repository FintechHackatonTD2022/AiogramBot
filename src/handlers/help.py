import aiogram

from . import users

from misc import i18n

_ = i18n.gettext


async def list_of_commands(message: aiogram.types.Message):
    i18n.ctx_locale.set('en')
    text = _('Привет вот список команд которые есть в боте:\n\n')
    for cmd in users:
        text += '/%s\n' % cmd
    await message.answer(text)
