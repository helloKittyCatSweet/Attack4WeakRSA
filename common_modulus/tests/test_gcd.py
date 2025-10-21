#!/usr/bin/env python3
"""
Unit Tests for Extended GCD
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from core import extended_gcd, mod_inverse


class TestExtendedGCD(unittest.TestCase):
    """Tests for the Extended Euclidean Algorithm"""
    
    def test_basic_gcd(self):
        """Test basic GCD computation"""
        test_cases = [
            (233, 151, 1),
            (240, 46, 2),
            (17, 13, 1),
            (1071, 462, 21),
            (65537, 3, 1),
        ]
        
        for a, b, expected_gcd in test_cases:
            with self.subTest(a=a, b=b):
                gcd, x, y = extended_gcd(a, b)
                self.assertEqual(gcd, expected_gcd)
    
    def test_bezout_identity(self):
        """Test Bézout's identity: ax + by = gcd(a, b)"""
        test_cases = [
            (233, 151),
            (240, 46),
            (17, 13),
            (1071, 462),
            (65537, 3),
        ]
        
        for a, b in test_cases:
            with self.subTest(a=a, b=b):
                gcd, x, y = extended_gcd(a, b)
                result = a * x + b * y
                self.assertEqual(result, gcd, 
                    f"Bézout identity verification failed: {a}*{x} + {b}*{y} = {result} != {gcd}")
    
    def test_paper_example(self):
        """Test example from the paper"""
        e1, e2 = 233, 151
        gcd, x, y = extended_gcd(e1, e2)
        
        self.assertEqual(gcd, 1)
        self.assertEqual(e1 * x + e2 * y, 1)
        # In the paper: x=35, y=-54, but other valid solutions exist
        self.assertTrue(abs(x) > 0 and abs(y) > 0)
    
    def test_coprime_numbers(self):
        """Test coprime pairs"""
        coprime_pairs = [
            (3, 5),
            (7, 11),
            (17, 257),
            (65537, 3),
        ]
        
        for a, b in coprime_pairs:
            with self.subTest(a=a, b=b):
                gcd, x, y = extended_gcd(a, b)
                self.assertEqual(gcd, 1)
                self.assertEqual(a * x + b * y, 1)


class TestModInverse(unittest.TestCase):
    """Tests for modular inverse computation"""
    
    def test_basic_mod_inverse(self):
        """Test basic modular inverse"""
        test_cases = [
            (3, 11, 4),   # 3 * 4 = 12 ≡ 1 (mod 11)
            (5, 7, 3),    # 5 * 3 = 15 ≡ 1 (mod 7)
            (7, 26, 15),  # 7 * 15 = 105 ≡ 1 (mod 26)
        ]
        
        for a, m, expected in test_cases:
            with self.subTest(a=a, m=m):
                inv = mod_inverse(a, m)
                self.assertIsNotNone(inv)
                self.assertEqual((a * inv) % m, 1)
    
    def test_no_inverse(self):
        """Test case where modular inverse does not exist"""
        # gcd(6, 9) = 3 != 1, so 6 has no inverse modulo 9
        inv = mod_inverse(6, 9)
        self.assertIsNone(inv)
    
    def test_inverse_verification(self):
        """Verify correctness of modular inverse"""
        test_cases = [
            (3, 7),
            (5, 11),
            (7, 13),
            (17, 23),
        ]
        
        for a, m in test_cases:
            with self.subTest(a=a, m=m):
                inv = mod_inverse(a, m)
                self.assertIsNotNone(inv)
                self.assertEqual((a * inv) % m, 1)


if __name__ == '__main__':
    unittest.main()
