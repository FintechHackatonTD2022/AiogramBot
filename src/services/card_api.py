import ast
import requests
from requests import Response

from bot_config import (BACKEND_PUBLIC_KEY_PATH, BACKEND_URL,
                        BOT_PRIVATE_KEY_PATH)
from .dict_operations import (decrypt_dict, encrypt_dict,
                              form_dictionary_createcard,
                              form_dictionary_getcard, load_privatekey,
                              load_publickey)


class CardApi:
    __url = BACKEND_URL + 'api/order/'

    @classmethod
    def create_card(cls, phone_number: str, iin: str, amount: str) -> dict:
        data = form_dictionary_createcard(
            398, amount, phone_number, iin)
        print(data)
        resp = requests.post(cls.__url + 'create_card/',
                             json=cls.__encrypt_request(data))
        print(resp)
        return cls.__decrypt_response(resp)

    @classmethod
    def get_card(cls, phone: str, iin: str) -> dict:
        data = form_dictionary_getcard(phone, iin)
        print(cls.__encrypt_request(data))
        resp = requests.post(cls.__url + 'get_card/',
                             json=cls.__encrypt_request(data))
        print(resp.text)
        return cls.__decrypt_response(resp)

    @classmethod
    def __encrypt_request(cls, request: dict) -> str:
        encrypted_str = encrypt_dict(
            request, load_publickey(BACKEND_PUBLIC_KEY_PATH))
        print(encrypted_str)
        return {'encrypted': encrypted_str.decode('utf-8')}

    @classmethod
    def __decrypt_response(cls, response: Response) -> dict:
        resolved_data = ast.literal_eval(response.text)
        encrypted_data = resolved_data['encrypted']
        return decrypt_dict(encrypted_data,
                            load_privatekey(BOT_PRIVATE_KEY_PATH))
