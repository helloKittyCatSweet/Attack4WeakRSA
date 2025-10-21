#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathematical utilities for cryptographic operations

Pure algorithm implementation with no I/O operations.
"""

import random
from typing import Tuple


class ImprovedMathUtils:
    """
    Improved mathematical utilities class
    
    Provides essential number-theoretic functions for cryptography:
    - GCD and extended GCD
    - Modular inverse
    - Primality testing (Miller-Rabin)
    - Prime number generation
    """

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Calculate greatest common divisor using Euclidean algorithm
        
        Args:
            a: First integer
            b: Second integer
            
        Returns:
            GCD of a and b
        """
        while b:
            a, b = b, a % b
        return abs(a)

    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """
        Extended Euclidean algorithm
        
        Finds integers x, y such that ax + by = gcd(a, b)
        
        Args:
            a: First integer
            b: Second integer
            
        Returns:
            Tuple (gcd, x, y) where gcd = ax + by
        """
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = ImprovedMathUtils.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y

    @staticmethod
    def mod_inverse(a: int, m: int) -> int:
        """
        Calculate modular inverse
        
        Finds x such that (a * x) % m = 1
        
        Args:
            a: Integer to invert
            m: Modulus
            
        Returns:
            Modular inverse of a modulo m
            
        Raises:
            ValueError: If modular inverse does not exist (gcd(a, m) != 1)
        """
        g, x, _ = ImprovedMathUtils.extended_gcd(a % m, m)
        if g != 1:
            raise ValueError("Modular inverse does not exist")
        return (x % m + m) % m

    @staticmethod
    def is_prime(n: int, k: int = 20) -> bool:
        """
        Miller-Rabin primality test
        
        Probabilistic primality test with error probability ≤ 4^(-k)
        
        Args:
            n: Integer to test
            k: Number of rounds (higher = more accurate)
            
        Returns:
            True if n is probably prime, False if n is composite
        """
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
            """Check if a witnesses that n is composite"""
            x = pow(a, d, n)
            if x in (1, n - 1):
                return False
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    return False
            return True

        # Test with k random bases
        for _ in range(k):
            a = random.randint(2, n - 2)
            if check_composite(a):
                return False
        return True

    @staticmethod
    def get_prime(bit_length: int) -> int:
        """
        Generate prime number with specified bit length
        
        Args:
            bit_length: Desired bit length of the prime
            
        Returns:
            Random prime number with the specified bit length
        """
        while True:
            p = random.getrandbits(bit_length)
            p |= (1 << (bit_length - 1)) | 1  # Ensure highest and lowest bits are 1
            if ImprovedMathUtils.is_prime(p):
                return p

