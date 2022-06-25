from aiogram import Dispatcher

from .i18n import I18nMiddleware

locales_dir = 'src/locales'

def setup(dispatcher: Dispatcher):
    i18n = I18nMiddleware("bot", locales_dir, default="en")
    dispatcher.middleware.setup(i18n)