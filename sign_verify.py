import encrypt_decrypt
import hmac
import hashlib
import json

key = b"secret_key"

def sign(payload):
    payload = encrypt_decrypt.decrypt_dict(payload)
    payload = json.dumps(payload, separators=(',', ':')).encode()
    signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
    return signature

def verify(payload):
    payload_signature = payload["signature"]
    payload_data = payload["data"]
    signature = sign(payload_data)
    return payload_signature == signature