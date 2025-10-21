"""
Unit tests for RSA key generation and encryption
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.rsa import (
    extended_gcd, modular_inverse, bytes_to_int, int_to_bytes,
    RSAKeyGenerator, RSAEncryptor
)


class TestCryptoUtils(unittest.TestCase):
    """Test cases for cryptographic utility functions"""

    def test_extended_gcd(self):
        """Test extended GCD"""
        g, x, y = extended_gcd(240, 46)
        self.assertEqual(g, 2)
        self.assertEqual(240 * x + 46 * y, g)

    def test_modular_inverse(self):
        """Test modular inverse"""
        inv = modular_inverse(3, 11)
        self.assertEqual((3 * inv) % 11, 1)
        
        inv = modular_inverse(7, 26)
        self.assertEqual((7 * inv) % 26, 1)

    def test_modular_inverse_no_inverse(self):
        """Test modular inverse when none exists"""
        with self.assertRaises(ValueError):
            modular_inverse(2, 4)

    def test_bytes_to_int(self):
        """Test bytes to integer conversion"""
        self.assertEqual(bytes_to_int(b'\x01\x02'), 258)
        self.assertEqual(bytes_to_int(b'\x00'), 0)

    def test_int_to_bytes(self):
        """Test integer to bytes conversion"""
        self.assertEqual(int_to_bytes(258), b'\x01\x02')
        self.assertEqual(int_to_bytes(0), b'\x00')

    def test_roundtrip_conversion(self):
        """Test roundtrip bytes <-> int conversion"""
        original = b'Hello, World!'
        n = bytes_to_int(original)
        recovered = int_to_bytes(n)
        self.assertEqual(original, recovered)


class TestRSAKeyGenerator(unittest.TestCase):
    """Test cases for RSA key generation"""

    def setUp(self):
        """Set up test fixtures"""
        self.gen = RSAKeyGenerator()

    def test_generate_keypair(self):
        """Test RSA keypair generation"""
        n, e, d, p, q = self.gen.generate_keypair(bits=16, max_gap=100)
        
        # Check n = p * q
        self.assertEqual(n, p * q)
        
        # Check e * d ≡ 1 (mod φ(n))
        phi = (p - 1) * (q - 1)
        self.assertEqual((e * d) % phi, 1)


class TestRSAEncryptor(unittest.TestCase):
    """Test cases for RSA encryption/decryption"""

    def test_encrypt_decrypt_int(self):
        """Test integer encryption/decryption"""
        # Use small known RSA parameters
        n, e, d = 3233, 17, 2753  # p=61, q=53
        
        message = 42
        ciphertext = RSAEncryptor.encrypt(message, e, n)
        decrypted = RSAEncryptor.decrypt(ciphertext, d, n)
        
        self.assertEqual(decrypted, message)

    def test_encrypt_decrypt_bytes(self):
        """Test bytes encryption/decryption"""
        n, e, d = 3233, 17, 2753

        # Use a smaller message that fits in n
        message = b'A'  # 65 < 3233
        ciphertext = RSAEncryptor.encrypt_bytes(message, e, n)
        decrypted = RSAEncryptor.decrypt_bytes(ciphertext, d, n)

        self.assertEqual(decrypted, message)


if __name__ == '__main__':
    unittest.main()

