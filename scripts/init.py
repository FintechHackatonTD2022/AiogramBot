import os
import os.path


if not os.path.isfile('.env'):
    with open('.env', 'w') as file:
        print('Paste following data')
        token = input('Telegram bot token: ')
        file.write('BOT_TOKEN = ' + token + '\n')
        backend_url = input('Back-end URL: ')
        file.write('BACKEND_URL = ' + backend_url + '\n')
        private_key_path = input('Private key path: ')
        file.write('BOT_PRIVATE_KEY_PATH = ' + private_key_path + '\n')
        public_key_path = input('Public key path: ')
        file.write('BACKEND_PUBLIC_KEY_PATH = ' + public_key_path + '\n')

    print('You can manually change it in .env file')
