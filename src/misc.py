from middlewares.i18n import I18nMiddleware

locales_dir = 'locales'
i18n = I18nMiddleware('bot', locales_dir)

locale = 'ru'
