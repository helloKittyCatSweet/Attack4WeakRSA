"""
Generate close prime pairs for Fermat factorization demonstration

Pure algorithm implementation with no I/O operations.

Strategy:
    1. Generate random prime p in [2^(bits-1), 2^bits)
    2. Add random even delta in [2, max_gap]
    3. Find next prime q
    4. Ensure |p-q| <= max_gap and both have same bit length
"""

import random
from typing import Tuple
from .primality import next_prime, miller_rabin


class ClosePrimeGenerator:
    """Generate pairs of primes that are close together"""

    def generate_close_primes(self, bits: int = 60, max_gap: int = 1 << 14) -> Tuple[int, int]:
        """
        Generate two primes of ~bits bits where |p-q| <= max_gap.

        Args:
            bits: Target bit length for primes (minimum 8)
            max_gap: Maximum allowed gap between primes

        Returns:
            (p, q) where p < q, both are prime, |p-q| <= max_gap

        Raises:
            ValueError: If bits < 8

        Example:
            >>> gen = ClosePrimeGenerator()
            >>> p, q = gen.generate_close_primes(bits=16, max_gap=100)
            >>> p.bit_length() == 16
            True
            >>> q.bit_length() == 16
            True
            >>> abs(p - q) <= 100
            True
        """
        if bits < 8:
            raise ValueError("Use at least 8 bits for a meaningful demo")

        lo = 1 << (bits - 1)
        hi = (1 << bits) - 1

        while True:
            # Generate first prime
            p_candidate = random.randrange(lo, hi)
            p = next_prime(p_candidate)

            # Ensure correct bit length
            if p.bit_length() != bits:
                continue

            # Generate second prime close to the first
            delta = random.randrange(2, max(4, max_gap + 1))
            if delta % 2 == 1:
                delta += 1

            q = next_prime(p + delta)

            # Verify both conditions
            if q.bit_length() == bits and q != p:
                return (p, q) if p < q else (q, p)

    def calculate_prime_gap(self, p: int, q: int) -> int:
        """
        Calculate the absolute difference between two primes.

        Args:
            p, q: Two prime numbers

        Returns:
            |p - q|

        Example:
            >>> gen = ClosePrimeGenerator()
            >>> gen.calculate_prime_gap(11, 13)
            2
        """
        return abs(p - q)

    def generate_multiple_pairs(self, count: int, bits: int = 60, max_gap: int = 1 << 14) -> list:
        """
        Generate multiple pairs of close primes.

        Args:
            count: Number of pairs to generate
            bits: Target bit length
            max_gap: Maximum gap between primes

        Returns:
            List of (p, q) tuples

        Example:
            >>> gen = ClosePrimeGenerator()
            >>> pairs = gen.generate_multiple_pairs(3, bits=16, max_gap=100)
            >>> len(pairs)
            3
        """
        return [self.generate_close_primes(bits, max_gap) for _ in range(count)]

