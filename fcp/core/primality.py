"""
Primality testing utilities using Miller-Rabin algorithm

Pure algorithm implementation with no I/O operations.

Implements:
    - Miller-Rabin probabilistic primality test
    - Next prime finder
"""

import random
from typing import List


# Small primes for quick divisibility checks
SMALL_PRIMES: List[int] = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


def miller_rabin(n: int, rounds: int = 16) -> bool:
    """
    Miller-Rabin probabilistic primality test.

    Args:
        n: Number to test for primality
        rounds: Number of test rounds (higher = more accurate)

    Returns:
        True if n is probably prime
        False if n is definitely composite

    Accuracy:
        Probability of error ≤ 4^(-rounds)
        With rounds=16: error probability ≤ 2.3e-10

    Example:
        >>> miller_rabin(17)
        True
        >>> miller_rabin(18)
        False
        >>> miller_rabin(1000000007)  # Large prime
        True
    """
    if n < 2:
        return False

    # Quick check against small primes
    for p in SMALL_PRIMES:
        if n == p:
            return True
        if n % p == 0:
            return False

    # Write n-1 = d * 2^s with d odd
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Test with random bases
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            # n is definitely composite
            return False
    
    # n is probably prime
    return True


def next_prime(start: int, rounds: int = 16) -> int:
    """
    Find the next prime number >= start.

    Args:
        start: Starting number
        rounds: Miller-Rabin test rounds

    Returns:
        The smallest prime >= start

    Example:
        >>> next_prime(10)
        11
        >>> next_prime(100)
        101
        >>> next_prime(1000)
        1009
    """
    if start < 2:
        return 2

    if start == 2:
        return 2

    # Make odd
    candidate = start if start % 2 == 1 else start + 1

    while not miller_rabin(candidate, rounds):
        candidate += 2

    return candidate


class PrimalityTester:
    """
    Miller-Rabin probabilistic primality testing (class interface).
    
    This class provides the same functionality as the module-level functions
    but with a class-based interface for compatibility with existing code.
    """

    SMALL_PRIMES = SMALL_PRIMES

    @classmethod
    def miller_rabin(cls, n: int, rounds: int = 16) -> bool:
        """Miller-Rabin primality test (class method)"""
        return miller_rabin(n, rounds)

    @classmethod
    def next_prime(cls, start: int, rounds: int = 16) -> int:
        """Find next prime (class method)"""
        return next_prime(start, rounds)

