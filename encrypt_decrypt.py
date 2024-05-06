"""
Functions to encrypt and decrypt payloads.
"""
import base64


def encrypt_object(obj)->str:
    """
    Encrypt a single object
    """
    return base64.b64encode(bytes(str(obj), 'utf-8')).decode('utf-8')

def encrypt_dict(payload: dict)->dict[str,str]:
    """
    Encrypt all elements in a dictionary
    """
    for field in payload:
        payload[field] = encrypt_object(payload[field])
    return payload

def decrypt_object(obj):
    """
    Decrypt single object. Will fail if object is not encrypted.
    """
    return base64.b64decode(obj).decode('utf-8')

def decrypt_dict(payload: dict)->dict:
    """
    Detect encrypted objects in a dictionary and decrypt them.
    Will return a dictionary of all plaintext elements in dict.
    """
    for field in payload:
        payload[field] = str(payload[field])
        try:
            decoded_data = base64.b64decode(payload[field]).decode('utf-8')
            payload[field]=decoded_data
        except:
            pass
    return payload

