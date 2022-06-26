from middlewares.i18n import I18nMiddleware

locales_dir = 'locales'
i18n = I18nMiddleware('bot', locales_dir)

locale = 'ru'
id_locales = {}


def get_locale(id: int) -> str:
    if id not in id_locales:
        return locale
    return id_locales[id]


def set_locale(id: int) -> str:
    id_locales[id] = locale
