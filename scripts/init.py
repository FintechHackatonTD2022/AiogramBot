import os
import os.path


if not os.path.isfile('.env'):
    with open('.env', 'w') as file:
        print('Paste following data')
        token = input('Telegram bot token: ')
        file.write('BOT_TOKEN = ' + token + '\n')
    print('You can manually change it in .env file')
