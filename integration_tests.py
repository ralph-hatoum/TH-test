import unittest
import requests
import json

url = 'http://localhost:8000'

# Helper functions to make tests more readable.

def make_http_request(payload, url):
    """
    Make a HTTP request to the given URL, with the given payload.
    """
    json_payload = json.dumps(payload, separators=(',', ':'))
    return requests.post(url, json_payload)

def make_http_request_no_json(payload, url):
    """
    Make a HTTP request to the given URL, with the given payload.
    """
    return requests.post(url, payload)

def encrypt_payload(payload):
    """
    Request the /encrypt endpoint
    """
    encrypt_endpoint = url+"/encrypt"
    return make_http_request(payload, encrypt_endpoint)

def decrypt_payload(payload):
    """
    Request the /decrypt endpoint
    """
    decrypt_endpoint = url+"/decrypt"
    return make_http_request(payload, decrypt_endpoint)

def sign_payload(payload):
    """
    Request the /sign endpoint
    """
    sign_endpoint = url+"/sign"
    return make_http_request(payload, sign_endpoint)

def verify_payload(payload):
    """
    Request the /verify endpoint
    """
    verify_endpoint = url+"/verify"
    return make_http_request(payload, verify_endpoint)

# Integration tests

class TestEncryptDecrypt(unittest.TestCase):
    """
    Tests on the /encrypt and /decrypt endpoints.
    """
    def test_encrypt_endpoint(self):
        """
        Testing a post on /encrypt.
        """
        payload = {"foo": "foobar","bar": {"isBar": True}}
        response = encrypt_payload(payload).json()
        self.assertEqual({'foo': 'Zm9vYmFy', 'bar': 'eydpc0Jhcic6IFRydWV9'}, response)

    def test_decrypt_endpoint(self):
        """
        Testing a post on /decrypt.
        When the plaintext value on a given key is not a string,
        we expect the decrypted value to be converted to string.
        """
        payload = {'foo': 'Zm9vYmFy', 'bar': 'eydpc0Jhcic6IFRydWV9'}
        response = decrypt_payload(payload).json()
        self.assertEqual({"foo": "foobar","bar": "{\'isBar\': True}"},response)


    def test_encrypt_decrypt(self):
        """
        Test that we can encrypt, then decrypt an endpoint and still get the
        initial values.
        When the plaintext value on a given key is not a string,
        we expect the decrypted value to be converted to string.
        """
        payload = {"foo": "foobar","bar": {"isBar": True}}

        # Encrypt the payload
        encrypted = encrypt_payload(payload)
        encrypted_json = encrypted.json()
        
        # Decrypt the result
        decrypted = decrypt_payload(encrypted_json)
        decrypted_json = decrypted.json()

        for key in payload:
            self.assertEqual(str(payload[key]),decrypted_json[key])


class TestSignVerify(unittest.TestCase):
    """
    Tests for the /sign and /verify endpoints.
    """
    def test_sign_endpoint(self):
        """
        Testing a post on /sign
        """
        payload = {'foo': 'Zm9vYmFy', 'bar': 'eydpc0Jhcic6IFRydWV9'}
        response = sign_payload(payload)
        self.assertEqual(200,response.status_code)

    def test_sign_verify_plaintext(self):
        """
        Test we can sign a plaintext payload, and verify it.
        Status code should be 204.
        """
        payload = {"foo": "foobar","bar": {"isBar": True}}

        # Sign the payload
        response = sign_payload(payload)
        signed = response.json()
        signature = signed["signature"]

        # Verify it 
        payload = {"signature":signature, 'data':payload}
        response =  verify_payload(payload)
        self.assertEqual(204,response.status_code)

    def test_sign_verify_plaintext_wrong_signature(self):
        """
        Test verifying with a wrong signature fails with 400.
        """
        payload = {"foo": "foobar","bar": {"isBar": True}}

        # Sign the payload
        response = sign_payload(payload)
        signed = response.json()
        signature = signed["signature"]

        # Verify it 
        payload = {"signature":signature+"e", 'data':payload}
        response =  verify_payload(payload)
        self.assertEqual(400,response.status_code)


    def test_sign_verify_encrypted(self):
        """
        Test we can sign an encrypted payload, and verify it.
        Status code should be 204.
        """
        payload = {'foo': 'Zm9vYmFy', 'bar': 'eydpc0Jhcic6IFRydWV9'}

        # Sign the payload
        response = sign_payload(payload)
        signed = response.json()
        signature = signed["signature"]

        # Verify it 
        payload = {"signature":signature, 'data':payload}
        response =  verify_payload(payload)
        self.assertEqual(204,response.status_code)

    def test_sign_verify_plaintext_encrypted_return_same(self):
        """
        Test that signing the payload in plaintext and verifying the same payload, encrypted, works.
        Status code should be 204.
        """
        payload = {"foo": "foobar","bar": {"isBar": True}} # Plaintext payload
        encrypted_payload = {'foo': 'Zm9vYmFy', 'bar': 'eydpc0Jhcic6IFRydWV9'} # Encrypted payload


        # Sign the plaintext payload
        response = sign_payload(payload)
        signed = response.json()
        signature = signed["signature"]

        # Verify with the encrypted payload
        payload = {"signature":signature, 'data':encrypted_payload}
        response = verify_payload(payload)
        self.assertEqual(204,response.status_code)

class WrongRequests(unittest.TestCase):
    """
    Sending requests that are not json and do not have required fields.
    """
    payload_not_json = "aaa"

    def test_send_payload_not_json_encrypt(self):
        response = make_http_request(self.payload_not_json, url+"/encrypt")
        self.assertEqual(400, response.status_code)

    def test_send_payload_not_json_decrypt(self):
        response = make_http_request(self.payload_not_json, url+"/decrypt")
        self.assertEqual(400, response.status_code)
    
    def test_send_payload_not_json_sign(self):
        response = make_http_request(self.payload_not_json, url+"/sign")
        self.assertEqual(400, response.status_code)

    def test_send_payload_not_json_verify(self):
        response = make_http_request(self.payload_not_json, url+"/verify")
        self.assertEqual(400, response.status_code)



if __name__ == '__main__':
    unittest.main()