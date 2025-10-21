#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathematical utilities for cryptographic operations
"""

import random
from typing import Tuple


class ImprovedMathUtils:
    """Improved mathematical utilities class"""

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculate greatest common divisor"""
        while b:
            a, b = b, a % b
        return abs(a)

    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """Extended Euclidean algorithm"""
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = ImprovedMathUtils.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y

    @staticmethod
    def mod_inverse(a: int, m: int) -> int:
        """Calculate modular inverse"""
        g, x, _ = ImprovedMathUtils.extended_gcd(a % m, m)
        if g != 1:
            raise ValueError("Modular inverse does not exist")
        return (x % m + m) % m

    @staticmethod
    def is_prime(n: int, k: int = 20) -> bool:
        """Miller-Rabin primality test"""
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False

        # Write n-1 as d*2^r
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        def check_composite(a: int) -> bool:
            x = pow(a, d, n)
            if x in (1, n - 1):
                return False
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    return False
            return True

        for _ in range(k):
            a = random.randint(2, n - 2)
            if check_composite(a):
                return False
        return True

    @staticmethod
    def get_prime(bit_length: int) -> int:
        """Generate prime number with specified bit length"""
        while True:
            p = random.getrandbits(bit_length)
            p |= (1 << (bit_length - 1)) | 1  # Ensure highest and lowest bits are 1
            if ImprovedMathUtils.is_prime(p):
                return p