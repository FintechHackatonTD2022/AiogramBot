import os
import logging
import logging.config

from dotenv import load_dotenv

from lib.bot import Bot
from services.schedule import Schedule
from middlewares.i18n import I18nMiddleware

# logger configuration
# logging.config.fileConfig('logging.conf')
logging.basicConfig(level=logging.WARNING,
                    format='%(name)s::%(levelname)s::%(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# VARS
BOT_TOKEN = os.getenv('BOT_TOKEN')
NOTION_API_TOKEN = os.getenv('NOTION_API_TOKEN')
DB_URL = os.getenv('DB_URL')

# Log info vars
logger.info('BOT_TOKEN = ' + BOT_TOKEN)
#logger.info('NOTION_API_TOKEN = ' + NOTION_API_TOKEN)
#logger.info('DB_URL = ' + DB_URL)


# main objects
bot = Bot(BOT_TOKEN)

# SINGLETON
schedule = Schedule()

# config
admins = [
    897651738
]
