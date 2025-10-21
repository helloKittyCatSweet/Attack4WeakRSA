"""
RSA key generation and encryption/decryption (pure algorithms)

Pure algorithm implementation with no I/O operations.

Implements:
    - RSA key pair generation with close primes
    - Encryption and decryption
    - Byte/integer conversion utilities
"""

import math
from typing import Tuple
from .prime_gen import ClosePrimeGenerator


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean algorithm.

    Args:
        a, b: Two integers

    Returns:
        (gcd, x, y) where gcd = a*x + b*y

    Example:
        >>> extended_gcd(240, 46)
        (2, -9, 47)
    """
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def modular_inverse(a: int, m: int) -> int:
    """
    Compute modular inverse using extended Euclidean algorithm.

    Args:
        a: Number to invert
        m: Modulus

    Returns:
        x where (a * x) % m == 1

    Raises:
        ValueError: If gcd(a, m) != 1

    Example:
        >>> modular_inverse(3, 11)
        4
        >>> (3 * 4) % 11
        1
    """
    a %= m
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"No modular inverse: gcd({a}, {m}) = {g} != 1")
    return x % m


def bytes_to_int(data: bytes) -> int:
    """
    Convert bytes to integer (big-endian).

    Args:
        data: Byte string

    Returns:
        Integer representation

    Example:
        >>> bytes_to_int(b'\\x01\\x02')
        258
    """
    return int.from_bytes(data, "big")


def int_to_bytes(x: int) -> bytes:
    """
    Convert integer to bytes (big-endian).

    Args:
        x: Non-negative integer

    Returns:
        Byte string representation

    Example:
        >>> int_to_bytes(258)
        b'\\x01\\x02'
    """
    if x == 0:
        return b"\x00"
    length = (x.bit_length() + 7) // 8
    return x.to_bytes(length, "big")


class RSAKeyGenerator:
    """RSA key pair generation using close primes"""

    def __init__(self):
        self.prime_gen = ClosePrimeGenerator()

    def generate_keypair(self, bits: int, max_gap: int, e: int = 65537) -> Tuple[int, int, int, int, int]:
        """
        Generate RSA keypair using close primes.

        Args:
            bits: Bit length for each prime
            max_gap: Maximum gap between primes
            e: Public exponent (default 65537)

        Returns:
            (n, e, d, p, q) where:
                n: Modulus (p * q)
                e: Public exponent
                d: Private exponent
                p, q: Prime factors

        Example:
            >>> gen = RSAKeyGenerator()
            >>> n, e, d, p, q = gen.generate_keypair(bits=16, max_gap=100)
            >>> n == p * q
            True
            >>> (e * d) % ((p-1)*(q-1)) == 1
            True
        """
        while True:
            p, q = self.prime_gen.generate_close_primes(bits, max_gap)
            n = p * q
            phi = (p - 1) * (q - 1)

            if math.gcd(e, phi) == 1:
                d = modular_inverse(e, phi)
                return n, e, d, p, q


class RSAEncryptor:
    """RSA encryption and decryption operations"""

    @staticmethod
    def encrypt(message: int, e: int, n: int) -> int:
        """
        Encrypt a message using RSA public key.

        Args:
            message: Plaintext (as integer, must be < n)
            e: Public exponent
            n: Modulus

        Returns:
            Ciphertext c = m^e mod n

        Example:
            >>> RSAEncryptor.encrypt(42, 65537, 3233)
            2557
        """
        return pow(message, e, n)

    @staticmethod
    def decrypt(ciphertext: int, d: int, n: int) -> int:
        """
        Decrypt a ciphertext using RSA private key.

        Args:
            ciphertext: Encrypted message
            d: Private exponent
            n: Modulus

        Returns:
            Plaintext m = c^d mod n

        Example:
            >>> RSAEncryptor.decrypt(2557, 2753, 3233)
            42
        """
        return pow(ciphertext, d, n)

    @staticmethod
    def encrypt_bytes(message: bytes, e: int, n: int) -> int:
        """
        Encrypt a byte string.

        Args:
            message: Plaintext bytes
            e: Public exponent
            n: Modulus

        Returns:
            Ciphertext (as integer)

        Example:
            >>> RSAEncryptor.encrypt_bytes(b'Hi', 65537, 3233)
            1675
        """
        m = bytes_to_int(message)
        return RSAEncryptor.encrypt(m, e, n)

    @staticmethod
    def decrypt_bytes(ciphertext: int, d: int, n: int) -> bytes:
        """
        Decrypt to a byte string.

        Args:
            ciphertext: Encrypted message (as integer)
            d: Private exponent
            n: Modulus

        Returns:
            Plaintext bytes

        Example:
            >>> RSAEncryptor.decrypt_bytes(1675, 2753, 3233)
            b'Hi'
        """
        m = RSAEncryptor.decrypt(ciphertext, d, n)
        return int_to_bytes(m)

