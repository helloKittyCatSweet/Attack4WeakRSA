"""
Unit tests for Fermat factorization algorithm
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.fermat import FermatFactorizer


class TestFermatFactorizer(unittest.TestCase):
    """Test cases for FermatFactorizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.factorizer = FermatFactorizer()

    def test_factor_small_numbers(self):
        """Test factorization of small numbers"""
        # 143 = 11 * 13
        result = self.factorizer.factor(143)
        self.assertIsNotNone(result)
        p, q = result
        self.assertEqual(p * q, 143)
        self.assertEqual(set([p, q]), {11, 13})

    def test_factor_close_primes(self):
        """Test factorization with close primes"""
        # 323 = 17 * 19 (gap = 2)
        result = self.factorizer.factor(323)
        self.assertIsNotNone(result)
        p, q = result
        self.assertEqual(p * q, 323)
        self.assertEqual(set([p, q]), {17, 19})

    def test_factor_even_number(self):
        """Test factorization of even numbers"""
        result = self.factorizer.factor(100)
        self.assertIsNotNone(result)
        p, q = result
        self.assertEqual(p * q, 100)
        self.assertEqual(p, 2)

    def test_factor_with_max_steps(self):
        """Test factorization with step limit"""
        # Large gap should fail with small max_steps
        result = self.factorizer.factor(143, max_steps=1)
        # May or may not succeed depending on starting point
        if result is not None:
            p, q = result
            self.assertEqual(p * q, 143)

    def test_factor_with_timing(self):
        """Test factorization with timing"""
        result, elapsed_ms = self.factorizer.factor_with_timing(143)
        self.assertIsNotNone(result)
        self.assertGreater(elapsed_ms, 0)
        p, q = result
        self.assertEqual(p * q, 143)

    def test_estimate_steps(self):
        """Test step estimation"""
        steps = self.factorizer.estimate_steps(11, 13)
        self.assertEqual(steps, 1)
        
        steps = self.factorizer.estimate_steps(17, 19)
        self.assertEqual(steps, 1)


if __name__ == '__main__':
    unittest.main()

