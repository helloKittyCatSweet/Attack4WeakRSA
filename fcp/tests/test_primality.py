"""
Unit tests for primality testing
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.primality import miller_rabin, next_prime, PrimalityTester


class TestPrimalityFunctions(unittest.TestCase):
    """Test cases for primality testing functions"""

    def test_miller_rabin_primes(self):
        """Test Miller-Rabin with known primes"""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 97, 1009, 10007]
        for p in primes:
            self.assertTrue(miller_rabin(p), f"{p} should be prime")

    def test_miller_rabin_composites(self):
        """Test Miller-Rabin with known composites"""
        composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 100, 1000]
        for n in composites:
            self.assertFalse(miller_rabin(n), f"{n} should be composite")

    def test_miller_rabin_edge_cases(self):
        """Test Miller-Rabin edge cases"""
        self.assertFalse(miller_rabin(0))
        self.assertFalse(miller_rabin(1))
        self.assertTrue(miller_rabin(2))

    def test_next_prime(self):
        """Test next_prime function"""
        self.assertEqual(next_prime(10), 11)
        self.assertEqual(next_prime(11), 11)
        self.assertEqual(next_prime(100), 101)
        self.assertEqual(next_prime(1000), 1009)

    def test_next_prime_edge_cases(self):
        """Test next_prime edge cases"""
        self.assertEqual(next_prime(0), 2)
        self.assertEqual(next_prime(1), 2)
        self.assertEqual(next_prime(2), 2)


class TestPrimalityTester(unittest.TestCase):
    """Test cases for PrimalityTester class"""

    def test_class_methods(self):
        """Test class method interface"""
        self.assertTrue(PrimalityTester.miller_rabin(17))
        self.assertFalse(PrimalityTester.miller_rabin(18))
        self.assertEqual(PrimalityTester.next_prime(10), 11)


if __name__ == '__main__':
    unittest.main()

