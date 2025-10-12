"""
Fermat factorization implementation for RSA moduli with close primes
"""

import math
import time

class FermatFactorizer:
    """Fermat factorization for numbers with close prime factors"""

    def factor(self, n, max_steps=None):
        """
        Fermat factorization for odd n.

        Returns (p, q) if a factorization is found where n = p*q and p<=q.
        If max_steps is given and exceeded, returns None.
        """
        if n % 2 == 0:
            return (2, n // 2)

        # Start from the square root
        a = math.isqrt(n)
        if a * a < n:
            a += 1

        steps = 0
        while True:
            b2 = a * a - n
            b = math.isqrt(b2)

            if b * b == b2:  # Found perfect square
                p = a - b
                q = a + b
                if p * q == n:
                    return (p, q) if p <= q else (q, p)

            a += 1
            steps += 1

            if max_steps is not None and steps > max_steps:
                return None

    def factor_with_timing(self, n):
        """Factor n and return both result and timing"""
        start_time = time.perf_counter()
        result = self.factor(n)
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        return result, elapsed_ms

    def run_multiple_trials(self, prime_generator, bits, max_gap, rounds):
        """Run multiple factorization trials and return timings"""
        timings = []

        for _ in range(rounds):
            p, q = prime_generator.generate_close_primes(bits, max_gap)
            n = p * q
            _, elapsed_ms = self.factor_with_timing(n)
            timings.append(elapsed_ms)

        return timings