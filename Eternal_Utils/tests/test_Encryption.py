import unittest
from Eternal_Utils.Encryption import Encryption


class TestEncryption(unittest.TestCase):
    def test___init__(self):
        assert True

    def test_decrypt_node(self):
        encryption = Encryption()
        enc = encryption.encrypt_node('API-Passkey')
        decrypted_enc = encryption.decrypt_node(enc)
        self.assertEqual('API-Passkey', decrypted_enc)

    def test_encrypt_node_length(self):
        encryption = Encryption()
        enc = encryption.encrypt_node('API-Passkey')
        self.assertEqual(32, len(enc))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
