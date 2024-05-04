"""
Functions to encrypt and decrypt payloads.
"""
import base64


def encrypt_object(obj)->str:
    """
    Encrypt a single object
    """
    return base64.b64encode(bytes(str(obj), 'utf-8')).decode('utf-8')

def encrypt_dict(dic: dict)->dict[str,str]:
    """
    Encrypt all elements in a dictionary
    """
    for key in dic:
        dic[key] = encrypt_object(dic[key])
    return dic

def decrypt_object(obj):
    """
    Decrypt single object. Will fail if object is not encrypted.
    """
    return base64.b64decode(obj).decode('utf-8')

def decrypt_dict(dic: dict)->dict:
    """
    Detect encrypted objects in a dictionary and decrypt them.
    Will return a dictionary of all plain text elements in dict.
    """
    for key in dic:
        try:
            decoded_data = base64.b64decode(dic[key]).decode('utf-8')
            dic[key]=decoded_data
        except:
            pass
    return dic


