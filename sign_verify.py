import encrypt_decrypt
import hmac
import hashlib
import json

key = b"secret_key"

def sign(payload):
    print(payload)
    payload = encrypt_decrypt.decrypt_dict(payload)
    print(payload)
    payload = json.dumps(payload, separators=(',', ':')).encode()
    signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
    return signature