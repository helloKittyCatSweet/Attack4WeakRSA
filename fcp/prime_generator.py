"""
Generate close prime pairs for Fermat factorization demonstration
"""

import random
from primality import PrimalityTester

class ClosePrimeGenerator:
    """Generate pairs of primes that are close together"""

    def __init__(self):
        self.tester = PrimalityTester()

    def generate_close_primes(self, bits=60, max_gap=1 << 14):
        """
        Generate two primes of ~`bits` bits where |p-q| <= max_gap.

        Strategy: pick a random prime p in [2^(bits-1), 2^bits),
        then move forward by a random even delta in [2, max_gap]
        and take the next prime as q.
        """
        if bits < 8:
            raise ValueError("Use at least 8 bits for a meaningful demo")

        lo = 1 << (bits - 1)
        hi = (1 << bits) - 1

        while True:
            # Generate first prime
            p_candidate = random.randrange(lo, hi)
            p = self.tester.next_prime(p_candidate)

            # Ensure correct bit length
            if p.bit_length() != bits:
                continue

            # Generate second prime close to the first
            delta = random.randrange(2, max(4, max_gap + 1))
            if delta % 2 == 1:
                delta += 1

            q = self.tester.next_prime(p + delta)

            if q.bit_length() == bits and q != p:
                return (p, q) if p < q else (q, p)

    def calculate_prime_gap(self, p, q):
        """Calculate the absolute difference between two primes"""
        return abs(p - q)

    def estimate_fermat_steps(self, gap):
        """Estimate number of Fermat factorization steps needed"""
        return gap // 2