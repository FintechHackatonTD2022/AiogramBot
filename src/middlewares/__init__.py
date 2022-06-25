from aiogram import Dispatcher

from misc import i18n


def setup(dispatcher: Dispatcher):
    dispatcher.middleware.setup(i18n)
