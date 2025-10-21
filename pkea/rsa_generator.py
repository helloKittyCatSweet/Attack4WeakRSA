#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSA parameter generator for demonstration purposes
"""

import random
from math_utils import ImprovedMathUtils


def generate_small_rsa_params(bit_length: int = 20, r: int = 2, s: int = 1):
    """
    Generate small RSA parameters for demonstration (ensuring attack success)
    """
    print(f"\n[*] Generating small RSA parameters (bit_length={bit_length}, r={r}, s={s})")

    p = ImprovedMathUtils.get_prime(bit_length)
    q = ImprovedMathUtils.get_prime(bit_length)
    while p == q:
        q = ImprovedMathUtils.get_prime(bit_length)

    N = (p ** r) * (q ** s)
    phi = (p ** (r - 1)) * (p - 1) * (q ** (s - 1)) * (q - 1)

    e = 65537
    while ImprovedMathUtils.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = ImprovedMathUtils.mod_inverse(e, phi)

    print(f"    p = {p}")
    print(f"    q = {q}")
    print(f"    N = {N}")
    print(f"    e = {e}")
    print(f"    d = {d}")
    print(f"    d bit length = {d.bit_length()} bits")

    return N, e, d, p, q, phi


def generate_standard_rsa(bit_length: int = 1024):
    """
    Generate standard RSA parameters
    """
    print(f"\n[*] Generating standard RSA parameters ({bit_length} bits)")

    p = ImprovedMathUtils.get_prime(bit_length // 2)
    q = ImprovedMathUtils.get_prime(bit_length // 2)
    while p == q:
        q = ImprovedMathUtils.get_prime(bit_length // 2)

    N = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    while ImprovedMathUtils.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = ImprovedMathUtils.mod_inverse(e, phi)

    print(f"    p = {p}")
    print(f"    q = {q}")
    print(f"    N = {N}")
    print(f"    e = {e}")
    print(f"    d bit length = {d.bit_length()} bits")

    return N, e, d, p, q, phi