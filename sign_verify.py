import encrypt_decrypt
import hmac
import hashlib
import json
import os

# Secret key will be grabbed from environment variable SECRET_KEY
key = os.getenv("SECRET_KEY", default = b"secret_key")

def sign(payload):
    """
    Given a payload, sign it and return the signature.
    As payload can contain encrypted fields, payload is decrypted first.
    """
    payload = encrypt_decrypt.decrypt_dict(payload)
    payload = json.dumps(payload, separators=(',', ':')).encode()
    signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
    return signature

def verify(payload):
    """
    Given a payload containing a signatrue and data, check if the signature
    matches the data.
    """
    payload_signature = payload.signature
    payload_data = payload.data
    signature = sign(payload_data)
    return payload_signature == signature