import base64
from datetime import datetime, timedelta, timezone
# import jwt
import rsa
import ast


def load_privatekey(path: str) -> rsa.key.PrivateKey:
    with open(path, "rb") as file:
        return rsa.PrivateKey.load_pkcs1(file.read())


def load_publickey(path: str) -> rsa.key.PublicKey:
    with open(path, "rb") as file:
        return rsa.PublicKey.load_pkcs1(file.read())


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


def encrypt_dict(dictionary: dict, public_key: rsa.key.PublicKey):
    return base64.b64encode(
        rsa.encrypt(bytes(str(dictionary), "utf-8"),  # what the fuck
                    public_key)
    )


def decrypt_dict(encrypted_dictionary: bytes,
                 private_key: rsa.key.PrivateKey) -> dict:
    return ast.literal_eval(
        rsa.decrypt(
            base64.b64decode(encrypted_dictionary),
            private_key
            ).decode("utf-8")
        )


# def encode_jws(enc_payload: bytes,
#                private_key: bytes,
#                algorithm='RS256') -> str:
#     return jwt.encode({"encrypted": enc_payload.decode("utf-8")},
#                       private_key,
#                       algorithm)


# def decode_jws(jws: str, public_key: bytes, algorithms='RS256') -> dict:
#     return jwt.decode(jws, public_key, algorithms)


def test(publickey_path: str, privatekey_path: str) -> None:
    dic = form_dictionary_createcard(
        398, "120000.00", "77773546064", "126733279987")
    pub = load_publickey(publickey_path)
    prv = load_privatekey(privatekey_path)
    enc = encrypt_dict(dic, pub)
    print(f"\nEncrypted dictionary: {enc}")
    dec = decrypt_dict(enc, prv)
    print(dec)


if __name__ == "__main__":
    test("bk_public.pem", "bk_private.pem")
