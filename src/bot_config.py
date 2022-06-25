import os
import logging
import logging.config

from dotenv import load_dotenv

from lib.bot import Bot
from services.schedule import Schedule

# logger configuration
# logging.config.fileConfig('logging.conf')
logging.basicConfig(level=logging.WARNING,
                    format='%(name)s::%(levelname)s::%(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# VARS
BOT_TOKEN = os.getenv('BOT_TOKEN')
BACKEND_URL = os.getenv('BACKEND_URL')

# Log info vars
logger.info('BOT_TOKEN = ' + BOT_TOKEN)
logger.info('BACKEND_URL = ' + BACKEND_URL)

# main objects
bot = Bot(BOT_TOKEN)

# SINGLETON
schedule = Schedule()

# config
admins = [
    897651738
]
