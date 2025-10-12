"""
Primality testing utilities using Miller-Rabin algorithm
"""

import random
import math


class PrimalityTester:
    """Miller-Rabin probabilistic primality testing"""

    # Small primes for quick checks
    SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

    @classmethod
    def miller_rabin(cls, n: int, rounds: int = 16) -> bool:
        """Probabilistic primality test. True means 'probably prime'."""
        if n < 2:
            return False

        # Quick check against small primes
        for p in cls.SMALL_PRIMES:
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
                return False
        return True

    @classmethod
    def next_prime(cls, start: int) -> int:
        """Return the smallest prime >= start (adjusting to odd)."""
        if start <= 2:
            return 2
        n = start
        if n % 2 == 0:
            n += 1
        while not cls.miller_rabin(n):
            n += 2
        return n