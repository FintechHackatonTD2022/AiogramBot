import aiogram

from bot_config import bot
from .menu import check_menu, FSM
import misc

_ = misc.i18n.gettext


async def start(message: aiogram.types.Message):
    misc.i18n.ctx_locale.set(misc.get_locale(message.from_id))
    buttons = [[_('💳 Открыть предоплаченную карту'), _('💰 Восстановить карту')],
               [_('⚙️ Настройки')]]
    bot.add_keyboard('menu', buttons)
    await message.answer(_('Привет, этот бот выпускает предоплаченные карты'),
                         reply_markup=bot.keyboards['menu'])
    bot.add_state_handler(FSM.menu, check_menu)
    await FSM.menu.set()
