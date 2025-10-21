#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSA parameter generator for demonstration purposes

Pure algorithm implementation with no I/O operations.
"""

import random
from typing import Tuple
from .math_utils import ImprovedMathUtils


def generate_small_rsa_params(bit_length: int = 20, r: int = 2, s: int = 1) -> Tuple[int, int, int, int, int, int]:
    """
    Generate small RSA parameters for demonstration (ensuring attack success)
    
    Generates RSA parameters with modulus N = p^r * q^s where p, q are primes.
    This variant is vulnerable to partial key exposure attacks.
    
    Args:
        bit_length: Bit length of each prime factor
        r: Exponent of p in modulus
        s: Exponent of q in modulus
        
    Returns:
        Tuple (N, e, d, p, q, phi) where:
        - N: RSA modulus = p^r * q^s
        - e: Public exponent
        - d: Private exponent
        - p, q: Prime factors
        - phi: Euler's totient φ(N)
    """
    # Generate two distinct primes
    p = ImprovedMathUtils.get_prime(bit_length)
    q = ImprovedMathUtils.get_prime(bit_length)
    while p == q:
        q = ImprovedMathUtils.get_prime(bit_length)

    # Calculate modulus and totient
    N = (p ** r) * (q ** s)
    phi = (p ** (r - 1)) * (p - 1) * (q ** (s - 1)) * (q - 1)

    # Choose public exponent
    e = 65537
    while ImprovedMathUtils.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # Calculate private exponent
    d = ImprovedMathUtils.mod_inverse(e, phi)

    return N, e, d, p, q, phi


def generate_standard_rsa(bit_length: int = 1024) -> Tuple[int, int, int, int, int, int]:
    """
    Generate standard RSA parameters
    
    Generates standard RSA parameters with modulus N = p * q.
    
    Args:
        bit_length: Total bit length of modulus (each prime is bit_length/2 bits)
        
    Returns:
        Tuple (N, e, d, p, q, phi) where:
        - N: RSA modulus = p * q
        - e: Public exponent
        - d: Private exponent
        - p, q: Prime factors
        - phi: Euler's totient φ(N)
    """
    # Generate two distinct primes
    p = ImprovedMathUtils.get_prime(bit_length // 2)
    q = ImprovedMathUtils.get_prime(bit_length // 2)
    while p == q:
        q = ImprovedMathUtils.get_prime(bit_length // 2)

    # Calculate modulus and totient
    N = p * q
    phi = (p - 1) * (q - 1)

    # Choose public exponent
    e = 65537
    while ImprovedMathUtils.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # Calculate private exponent
    d = ImprovedMathUtils.mod_inverse(e, phi)

    return N, e, d, p, q, phi

