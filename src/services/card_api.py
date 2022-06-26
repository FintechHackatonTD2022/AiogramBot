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
    def create_card(cls, phone_number: str, iin: str, amount: str):
        data = form_dictionary_createcard(
            398, amount, phone_number, iin)
        resp = requests.post(cls.__url + 'create_card/',
                             json=cls.__encrypt_request(data))
        return cls.__decrypt_response(resp)

    @classmethod
    def get_card(cls):
        data = form_dictionary_getcard('87085448617')
        encrypted_data = cls.__encrypt_data(data)
        data = {'encrypted': encrypted_data}
        resp = requests.get(cls.__url + 'get_card/', json=data)
        return cls.__decrypt_data(resp.text)

    @classmethod
    def __encrypt_request(cls, request: dict) -> str:
        encrypted_str = encrypt_dict(
            request, load_publickey(BACKEND_PUBLIC_KEY_PATH))
        return {'encrypted': encrypted_str.decode('utf-8')}

    @classmethod
    def __decrypt_response(cls, response: Response) -> dict:
        resolved_data = ast.literal_eval(response.text)
        encrypted_data = resolved_data['encrypted']
        return decrypt_dict(encrypted_data,
                            load_privatekey(BOT_PRIVATE_KEY_PATH))
