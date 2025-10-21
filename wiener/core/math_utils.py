"""
Mathematical utility functions

Pure mathematical functions with no I/O.
"""

import math


def isqrt(n: int) -> int:
    """
    Integer square root using Newton's method
    
    Args:
        n: Non-negative integer
        
    Returns:
        Floor of square root of n
    """
    if n < 0:
        return 0
    if n == 0:
        return 0
    
    # Newton's method
    x = n
    y = (x + 1) // 2
    
    while y < x:
        x = y
        y = (x + n // x) // 2
    
    return x


def gcd(a: int, b: int) -> int:
    """
    Greatest common divisor using Euclidean algorithm
    
    Args:
        a, b: Integers
        
    Returns:
        GCD of a and b
    """
    while b:
        a, b = b, a % b
    return abs(a)


def modinv(a: int, m: int) -> int:
    """
    Modular multiplicative inverse using extended Euclidean algorithm
    
    Args:
        a: Integer
        m: Modulus
        
    Returns:
        x such that (a * x) % m == 1
        
    Raises:
        ValueError: If inverse doesn't exist
    """
    if gcd(a, m) != 1:
        raise ValueError(f"Modular inverse of {a} mod {m} doesn't exist")
    
    # Extended Euclidean algorithm
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    _, x, _ = extended_gcd(a % m, m)
    return (x % m + m) % m

