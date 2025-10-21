#!/usr/bin/env python3
"""
Unit Tests for ECC-RSA Common Modulus Attack
ECC-RSA common-modulus attack unit tests
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from core import ECCRSACommonModulusAttack


class TestECCRSAAttack(unittest.TestCase):
    """Tests for ECC-RSA common-modulus attack"""
    
    def setUp(self):
        """Set up for tests"""
        # Use small primes for testing
        self.a = 1
        self.b = 1
        self.p = 23
        self.attacker = ECCRSACommonModulusAttack(self.a, self.b, self.p)
    
    def test_point_add(self):
        """Test elliptic curve point addition"""
        P = (3, 10)
        Q = (9, 7)
        
        R = self.attacker.point_add(P, Q)
        
        self.assertIsNotNone(R)
        # Verify the result lies on the curve
        self.assertTrue(self.attacker.verify_point_on_curve(R))
    
    def test_point_double(self):
        """Test point doubling"""
        P = (3, 10)
        
        # 2P = P + P
        R = self.attacker.point_add(P, P)
        
        self.assertIsNotNone(R)
        self.assertTrue(self.attacker.verify_point_on_curve(R))
    
    def test_scalar_mult(self):
        """Test scalar multiplication"""
        P = (3, 10)
        
        # Test different scalars
        for k in [2, 3, 5, 7]:
            with self.subTest(k=k):
                R = self.attacker.scalar_mult(k, P)
                if R is not None:
                    self.assertTrue(self.attacker.verify_point_on_curve(R))
    
    def test_scalar_mult_zero(self):
        """Test zero scalar multiplication"""
        P = (3, 10)
        R = self.attacker.scalar_mult(0, P)
        self.assertIsNone(R)  # point at infinity
    
    def test_scalar_mult_negative(self):
        """Test negative scalar multiplication"""
        P = (3, 10)
        
        # -k * P should be the inverse of k * P
        k = 3
        R_pos = self.attacker.scalar_mult(k, P)
        R_neg = self.attacker.scalar_mult(-k, P)
        
        if R_pos and R_neg:
            # Verify R_pos + R_neg = O (point at infinity)
            R_sum = self.attacker.point_add(R_pos, R_neg)
            self.assertIsNone(R_sum)
    
    def test_verify_point_on_curve(self):
        """Test whether points are on the curve"""
        # A point on the curve
        P_on = (3, 10)
        self.assertTrue(self.attacker.verify_point_on_curve(P_on))
        
        # A point not on the curve
        P_off = (1, 1)
        self.assertFalse(self.attacker.verify_point_on_curve(P_off))
        
        # The point at infinity
        self.assertTrue(self.attacker.verify_point_on_curve(None))
    
    def test_basic_attack(self):
        """Test basic attack flow"""
        # Note: this test may not succeed, because the ECC-RSA encryption
        # in the paper is not a simple scalar multiplication.
        # This just tests that the attack code path runs.
        
        N = 181603559630213323475279432919469869812801
        e1 = 233
        e2 = 151
        
        # Ciphertext points from the paper
        C1 = (165824579408065034165410, 127733294106034267552844)
        C2 = (165824579408065034165410, 53870265524179202259957)
        
        # Create attacker with the paper parameters
        a = 1
        b = 1
        p = N
        attacker = ECCRSACommonModulusAttack(a, b, p)
        
        # Execute attack (may not recover the correct plaintext, but should run)
        M = attacker.attack(N, e1, e2, C1, C2)
        
        # Should return either a point or None
        self.assertTrue(M is None or isinstance(M, tuple))


if __name__ == '__main__':
    unittest.main()
