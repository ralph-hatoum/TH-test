import unittest
import encrypt_decrypt
import json

# Test case class
class TestEncryption(unittest.TestCase):
    """
    Testing encryption
    """

    def compare_actual_expected(self, input_data, expected_output):
        """
        Compare function's result to expected output.
        """
        with open(input_data,"r", encoding='utf-8') as f:
            json_payload = json.load(f)
        encrypted_data = encrypt_decrypt.encrypt_dict(json_payload)
        with open(expected_output,"r",encoding='utf-8') as f:
            expected_output = json.load(f)
        self.assertEqual(encrypted_data, expected_output)

    def test_encrypt_simple_payload(self):
        """
        Encrypting a simple payload.
        """
        self.compare_actual_expected("example.json", "expected_example.json")  
    def test_encrypt_complex_playload(self):
        """
        Encrypting a complex payload.
        """
        self.compare_actual_expected("test.json","expected_test.json")



if __name__ == '__main__':
    unittest.main()