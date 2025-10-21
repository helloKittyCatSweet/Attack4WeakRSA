"""
Unit tests for close prime generation
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.prime_gen import ClosePrimeGenerator
from core.primality import miller_rabin


class TestClosePrimeGenerator(unittest.TestCase):
    """Test cases for ClosePrimeGenerator"""

    def setUp(self):
        """Set up test fixtures"""
        self.gen = ClosePrimeGenerator()

    def test_generate_close_primes_basic(self):
        """Test basic close prime generation"""
        p, q = self.gen.generate_close_primes(bits=16, max_gap=100)
        
        # Check both are prime
        self.assertTrue(miller_rabin(p))
        self.assertTrue(miller_rabin(q))
        
        # Check bit length
        self.assertEqual(p.bit_length(), 16)
        self.assertEqual(q.bit_length(), 16)
        
        # Check gap
        gap = abs(p - q)
        self.assertLessEqual(gap, 100)

    def test_generate_close_primes_different_sizes(self):
        """Test generation with different bit sizes"""
        for bits in [8, 12, 16, 20]:
            p, q = self.gen.generate_close_primes(bits=bits, max_gap=50)
            self.assertEqual(p.bit_length(), bits)
            self.assertEqual(q.bit_length(), bits)
            self.assertTrue(miller_rabin(p))
            self.assertTrue(miller_rabin(q))

    def test_generate_close_primes_invalid_bits(self):
        """Test with invalid bit length"""
        with self.assertRaises(ValueError):
            self.gen.generate_close_primes(bits=7, max_gap=100)

    def test_calculate_prime_gap(self):
        """Test gap calculation"""
        gap = self.gen.calculate_prime_gap(11, 13)
        self.assertEqual(gap, 2)
        
        gap = self.gen.calculate_prime_gap(13, 11)
        self.assertEqual(gap, 2)

    def test_generate_multiple_pairs(self):
        """Test generating multiple pairs"""
        pairs = self.gen.generate_multiple_pairs(3, bits=12, max_gap=50)
        self.assertEqual(len(pairs), 3)
        
        for p, q in pairs:
            self.assertTrue(miller_rabin(p))
            self.assertTrue(miller_rabin(q))
            self.assertEqual(p.bit_length(), 12)
            self.assertEqual(q.bit_length(), 12)


if __name__ == '__main__':
    unittest.main()

