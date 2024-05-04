import requests
import json

url = 'http://localhost:8000'


def test_encrypt_endpoint():
    encrypt_endpoint = url+"/encrypt"
    payload = {"foo": "foobar","bar": {"isBar": True}}
    json_payload = json.dumps(payload, separators=(',', ':'))
    print(json_payload)
    response = requests.post(encrypt_endpoint, json_payload)
    print(response.status_code)
    print(response.json())

def test_decrypt_endpoint():
    decrypt_endpoint = url+"/decrypt"
    payload = {'foo': 'Zm9vYmFy', 'bar': 'eydpc0Jhcic6IFRydWV9'}
    json_payload = json.dumps(payload, separators=(',', ':'))
    response = requests.post(decrypt_endpoint, json_payload)
    print(response.status_code)
    print(response.json())

def test_sign_endpoint():
    sign_endpoint = url+"/sign"
    payload = {'foo': 'Zm9vYmFy', 'bar': 'eydpc0Jhcic6IFRydWV9'}
    json_payload = json.dumps(payload, separators=(',', ':'))
    print(json_payload)
    response = requests.post(sign_endpoint, json_payload)
    print(response.status_code)
    print(response.json())

