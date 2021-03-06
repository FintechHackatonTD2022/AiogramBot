from bot_config import admins, bot
import handlers
from handlers.help import list_of_commands
from utils.notify import notify_admins
from utils.commands import DefaultCommands
import middlewares

default_commands = {
    'list': 'list of possible bot commands',
    'get_card': 'получить карту',
}

tasks_on_startup = [
    DefaultCommands.set(default_commands).on_startup,
]


def start(bot=bot):
    bot.admins = admins

    for task in tasks_on_startup:
        bot.add_on_startup(task)

    middlewares.setup(bot.dp)

    bot.add_command_handler('list', list_of_commands)
    for cmd in handlers.users:
        bot.add_command_handler(cmd, handlers.users[cmd])
    for cmd in handlers.admins:
        bot.add_command_handler(cmd, handlers.admins[cmd], admin_only=True)

    notify_admins('bot started')
    bot.start()
    notify_admins('bot stopped')
