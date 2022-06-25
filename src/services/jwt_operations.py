from datetime import datetime, timedelta, timezone
import jwt


def read_key_from_file(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


def form_dictionary_createcard(currency: int, amount: str,
                               phone_number: str, inn: str) -> dict:
    return {
        "currency": currency,
        "amount": amount,
        "msisdn": phone_number,
        "extra_data": {
            'INN': inn
        },
        'iat': int(datetime.now(timezone.utc).timestamp()),
        'exp': int((datetime.now(timezone.utc) + timedelta(hours=1)
                    ).timestamp())
    }


def form_dictionary_getcard(phone_number: str) -> dict:
    return {
        "msisdn": phone_number,
        'iat': int(datetime.now(timezone.utc).timestamp()),
        'exp': int((datetime.now(timezone.utc) + timedelta(hours=1)
                    ).timestamp())
    }


def encode_jws(payload: dict, signing_key: str, algorithm='RS256') -> str:
    return jwt.encode(payload, signing_key, algorithm)


def decrypt_jws(jws: str, verifying_key: str) -> dict:
    return jwt.decode(jws, verifying_key, do_time_check=True)
