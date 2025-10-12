"""
RSA encryption/decryption demonstration with Fermat factorization attack
"""

import math
from prime_generator import ClosePrimeGenerator

class RSADemo:
    """Complete RSA demo: keygen -> encrypt -> factor -> decrypt"""

    def __init__(self):
        self.prime_gen = ClosePrimeGenerator()

    def _extended_gcd(self, a, b):
        """Extended Euclidean algorithm"""
        if b == 0:
            return (a, 1, 0)
        g, x1, y1 = self._extended_gcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

    def _modular_inverse(self, a, m):
        """Compute modular inverse using extended Euclidean algorithm"""
        a %= m
        g, x, _ = self._extended_gcd(a, m)
        if g != 1:
            raise ValueError("No modular inverse for given inputs")
        return x % m

    def generate_rsa_keypair(self, bits, max_gap, e=65537):
        """Generate RSA keypair using close primes for demonstration"""
        while True:
            p, q = self.prime_gen.generate_close_primes(bits, max_gap)
            n = p * q
            phi = (p - 1) * (q - 1)

            if math.gcd(e, phi) == 1:
                d = self._modular_inverse(e, phi)
                return n, e, d, p, q

    def _bytes_to_int(self, data):
        """Convert bytes to integer"""
        return int.from_bytes(data, "big")

    def _int_to_bytes(self, x):
        """Convert integer to bytes"""
        if x == 0:
            return b"\x00"
        length = (x.bit_length() + 7) // 8
        return x.to_bytes(length, "big")

    def encrypt_message(self, message, n, e):
        """Encrypt a string message using RSA"""
        message_bytes = message.encode("utf-8")
        m = self._bytes_to_int(message_bytes)

        if m >= n:
            raise ValueError("Message too large for modulus")

        return pow(m, e, n)

    def decrypt_message(self, ciphertext, n, d):
        """Decrypt RSA ciphertext to string"""
        m_dec = pow(ciphertext, d, n)
        message_bytes = self._int_to_bytes(m_dec)
        return message_bytes.decode("utf-8", errors="replace")