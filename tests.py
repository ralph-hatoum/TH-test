import unittest
import encrypt_decrypt
import json

# Test case class
class TestEncryption(unittest.TestCase):
    """
    Testing encryption
    """
    test_data_dir = "test_data/encrypt/"

    def compare_actual_expected(self, input_data, expected_output):
        """
        Compare function's result to expected output.
        """
        with open(self.test_data_dir+input_data,"r", encoding='utf-8') as f:
            json_payload = json.load(f)
        encrypted_data = encrypt_decrypt.encrypt_dict(json_payload)
        with open(self.test_data_dir+expected_output,"r",encoding='utf-8') as f:
            expected_output = json.load(f)
        self.assertEqual(encrypted_data, expected_output)

    def test_encrypt_simple_payload(self):
        """
        Encrypting a simple payload.
        """
        self.compare_actual_expected("simple_payload.json", "expected_simple_payload.json")  
    def test_encrypt_complex_playload(self):
        """
        Encrypting a complex payload.
        """
        self.compare_actual_expected("complex_payload.json","expected_complex_payload.json")

class TestDecryption(unittest.TestCase):
    """
    Testing decryption
    """
    test_data_dir = "test_data/decrypt/"

    def compare_actual_expected(self, input_data, expected_output):
        """
        Compare function's result to expected output.
        """
        with open(self.test_data_dir+input_data,"r", encoding='utf-8') as f:
            json_payload = json.load(f)
        encrypted_data = encrypt_decrypt.decrypt_dict(json_payload)
        with open(self.test_data_dir+expected_output,"r",encoding='utf-8') as f:
            expected_output = json.load(f)
        self.assertEqual(encrypted_data, expected_output)

    def test_decrypt_fully_encrypted_payload(self):
        """
        Decrypting a payload where all fields are encrypted.
        """
        self.compare_actual_expected("fully_encrypted.json", "expected_fully_encrypted.json")  
    def test_decrypt_partially_encrypted_payload(self):
        """
        Decrypting a payload where not all fields are encrypted.
        """
        self.compare_actual_expected("partially_encrypted.json","expected_partially_encrypted.json")

if __name__ == '__main__':
    unittest.main()