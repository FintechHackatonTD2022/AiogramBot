from . import jwt_operations
import requests

from bot_config import BOT_PRIVATE_KEY_PATH, BACKEND_PUBLIC_KEY_PATH, BACKEND_URL
from .jwt_operations import read_key_from_file, encode_jws, decrypt_jws


class CardApi:
    __url = BACKEND_URL + 'api/order/'

    @classmethod
    def create_card(cls):
        data = jwt_operations.form_dictionary_createcard(
            120000, '0', '87085448617', '030616551031')
        encrypted_data = cls.__encrypt_data(data)
        resp = requests.post(cls.__url + 'create_card/', data=encrypted_data)
        return cls.__decrypt_data(resp.text)

    @classmethod
    def get_card(cls):
        data = jwt_operations.form_dictionary_getcard('87085448617')
        cls.__encrypt_data(data)
        resp = requests.get(cls.__url + 'get_card/', json=data)
        return cls.__decrypt_data(resp.text)

    @classmethod
    def __encrypt_data(cls, data: dict) -> str:
        return encode_jws(data, read_key_from_file(BOT_PRIVATE_KEY_PATH))

    @classmethod
    def __decrypt_data(cls, encrypted_data: str) -> dict:
        return decrypt_jws(encrypted_data,
                           read_key_from_file(BACKEND_PUBLIC_KEY_PATH))
