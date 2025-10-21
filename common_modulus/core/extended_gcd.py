#!/usr/bin/env python3
"""
Extended Euclidean Algorithm

For solving ax + by = gcd(a, b) to find x and y
"""


def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm

    Solve: ax + by = gcd(a, b)

    Args:
        a: First integer
        b: Second integer

    Returns:
        (gcd, x, y): Greatest common divisor and Bezout coefficients
        satisfying a*x + b*y = gcd(a, b)

    Example:
        >>> extended_gcd(233, 151)
        (1, 35, -54)
        Verify: 233*35 + 151*(-54) = 8155 - 8154 = 1 ✓
    """
    if b == 0:
        return a, 1, 0

    # Save original values for verification
    orig_a, orig_b = a, b

    # Initialize
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    # Iterative computation
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd = old_r
    x = old_s
    y = old_t

    # Verify result
    assert orig_a * x + orig_b * y == gcd, f"Verification failed: {orig_a}*{x} + {orig_b}*{y} != {gcd}"

    return gcd, x, y


def mod_inverse(a, m):
    """
    Compute modular inverse

    Solve a * x ≡ 1 (mod m) for x

    Args:
        a: Integer
        m: Modulus

    Returns:
        x: Modular inverse, None if it doesn't exist

    Example:
        >>> mod_inverse(3, 11)
        4
        Verify: 3 * 4 = 12 ≡ 1 (mod 11) ✓
    """
    gcd, x, _ = extended_gcd(a, m)

    if gcd != 1:
        return None  # Modular inverse doesn't exist

    return x % m

