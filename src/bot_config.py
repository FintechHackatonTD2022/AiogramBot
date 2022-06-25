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
BOT_PRIVATE_KEY_PATH = os.getenv('BOT_PRIVATE_KEY_PATH')
BACKEND_PUBLIC_KEY_PATH = os.getenv('BACKEND_PUBLIC_KEY_PATH')

# Log info vars
logger.info('BOT_TOKEN = ' + BOT_TOKEN)
logger.info('BACKEND_URL = ' + BACKEND_URL)
logger.info('BOT_PRIVATE_KEY_PATH =' + BOT_PRIVATE_KEY_PATH)
logger.info('BOT_PRIVATE_KEY_PATH =' + BACKEND_PUBLIC_KEY_PATH)

# main objects
bot = Bot(BOT_TOKEN)

# SINGLETON
schedule = Schedule()

# config
admins = [
    897651738
]
