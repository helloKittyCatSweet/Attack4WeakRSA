"""
Fermat factorization implementation for RSA moduli with close primes

Pure algorithm implementation with no I/O operations.

Algorithm:
    For n = p*q where p and q are close primes:
    1. Start from a = ceil(sqrt(n))
    2. Check if a^2 - n is a perfect square
    3. If yes, n = (a-b)(a+b) where b = sqrt(a^2 - n)
    4. Otherwise, increment a and repeat

Time Complexity: O(|p-q|/2) iterations
"""

import math
import time
from typing import Optional, Tuple


class FermatFactorizer:
    """Fermat factorization for numbers with close prime factors"""

    def factor(self, n: int, max_steps: Optional[int] = None) -> Optional[Tuple[int, int]]:
        """
        Fermat factorization for odd n.

        Args:
            n: The number to factor (should be odd composite)
            max_steps: Maximum number of iterations (None = unlimited)

        Returns:
            (p, q) if factorization found where n = p*q and p <= q
            None if max_steps exceeded without finding factors

        Example:
            >>> factorizer = FermatFactorizer()
            >>> factorizer.factor(143)  # 143 = 11 * 13
            (11, 13)
        """
        # Handle even numbers
        if n % 2 == 0:
            return (2, n // 2)

        # Start from ceiling of square root
        a = math.isqrt(n)
        if a * a < n:
            a += 1

        steps = 0
        while True:
            b2 = a * a - n
            b = math.isqrt(b2)

            # Check if b^2 = a^2 - n (perfect square)
            if b * b == b2:
                p = a - b
                q = a + b
                # Verify factorization
                if p * q == n:
                    return (p, q) if p <= q else (q, p)

            a += 1
            steps += 1

            # Check step limit
            if max_steps is not None and steps > max_steps:
                return None

    def factor_with_timing(self, n: int, max_steps: Optional[int] = None) -> Tuple[Optional[Tuple[int, int]], float]:
        """
        Factor n and return both result and timing.

        Args:
            n: The number to factor
            max_steps: Maximum number of iterations

        Returns:
            (result, elapsed_ms) where:
                result: (p, q) or None
                elapsed_ms: Time taken in milliseconds

        Example:
            >>> factorizer = FermatFactorizer()
            >>> result, time_ms = factorizer.factor_with_timing(143)
            >>> result
            (11, 13)
            >>> time_ms < 1.0  # Very fast for small numbers
            True
        """
        start_time = time.perf_counter()
        result = self.factor(n, max_steps)
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        return result, elapsed_ms

    def estimate_steps(self, p: int, q: int) -> int:
        """
        Estimate the number of Fermat iterations needed.

        Args:
            p, q: The two prime factors

        Returns:
            Estimated number of steps ≈ |p-q|/2

        Example:
            >>> factorizer = FermatFactorizer()
            >>> factorizer.estimate_steps(11, 13)
            1
        """
        return abs(p - q) // 2

