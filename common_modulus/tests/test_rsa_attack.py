#!/usr/bin/env python3
"""
Unit Tests for RSA Common Modulus Attack
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from Crypto.Util.number import getPrime, GCD
from core import CommonModulusAttack


class TestCommonModulusAttack(unittest.TestCase):
    """Tests for the plain RSA common-modulus attack"""
    
    def setUp(self):
        """Test setup"""
        self.attacker = CommonModulusAttack()
    
    def test_small_example(self):
        """Test a small numeric example"""
        N = 3233
        e1 = 3
        e2 = 5
        M = 42
        
        C1 = pow(M, e1, N)
        C2 = pow(M, e2, N)
        
        recovered_M = self.attacker.attack(N, e1, e2, C1, C2)
        
        self.assertIsNotNone(recovered_M)
        self.assertEqual(recovered_M, M)
    
    def test_512_bit_rsa(self):
        """Test with a 512-bit RSA modulus"""
        p = getPrime(256)
        q = getPrime(256)
        N = p * q
        phi = (p - 1) * (q - 1)
        
        e1 = 3
        e2 = 5
        
        # Ensure e1, e2 are coprime with phi
        while GCD(e1, phi) != 1:
            e1 += 2
        while GCD(e2, phi) != 1 or e2 == e1:
            e2 += 2
        
        M = 123456789
        C1 = pow(M, e1, N)
        C2 = pow(M, e2, N)
        
        recovered_M = self.attacker.attack(N, e1, e2, C1, C2)
        
        self.assertIsNotNone(recovered_M)
        self.assertEqual(recovered_M, M)
    
    def test_different_e_values(self):
        """Test several different e-value pairs"""
        p = getPrime(128)
        q = getPrime(128)
        N = p * q
        phi = (p - 1) * (q - 1)
        
        e_pairs = [(3, 5), (7, 11), (17, 257)]
        M = 987654321
        
        for e1, e2 in e_pairs:
            with self.subTest(e1=e1, e2=e2):
                # Ensure e1, e2 are coprime with phi
                while GCD(e1, phi) != 1:
                    e1 += 2
                while GCD(e2, phi) != 1 or e2 == e1:
                    e2 += 2
                
                C1 = pow(M, e1, N)
                C2 = pow(M, e2, N)
                
                recovered_M = self.attacker.attack(N, e1, e2, C1, C2)
                
                self.assertIsNotNone(recovered_M)
                self.assertEqual(recovered_M, M)
    
    def test_attack_failure_non_coprime(self):
        """Test attack failure when e1 and e2 are not coprime"""
        N = 3233
        e1 = 6  # gcd(6, 9) = 3
        e2 = 9
        M = 42
        
        C1 = pow(M, e1, N)
        C2 = pow(M, e2, N)
        
        recovered_M = self.attacker.attack(N, e1, e2, C1, C2)
        
        self.assertIsNone(recovered_M)
    
    def test_verify_method(self):
        """Test the verification method"""
        N = 3233
        e1 = 3
        e2 = 5
        M = 42
        
        C1 = pow(M, e1, N)
        C2 = pow(M, e2, N)
        
        recovered_M = self.attacker.attack(N, e1, e2, C1, C2)
        
        # Verify the recovered plaintext
        is_valid = self.attacker.verify(recovered_M, N, e1, e2, C1, C2)
        self.assertTrue(is_valid)
    
    def test_large_message(self):
        """Test with a large message (but less than N)"""
        p = getPrime(256)
        q = getPrime(256)
        N = p * q
        phi = (p - 1) * (q - 1)
        
        e1 = 3
        e2 = 5
        
        while GCD(e1, phi) != 1:
            e1 += 2
        while GCD(e2, phi) != 1 or e2 == e1:
            e2 += 2
        
        # Large message (but < N)
        M = N // 2
        
        C1 = pow(M, e1, N)
        C2 = pow(M, e2, N)
        
        recovered_M = self.attacker.attack(N, e1, e2, C1, C2)
        
        self.assertIsNotNone(recovered_M)
        self.assertEqual(recovered_M, M)


if __name__ == '__main__':
    unittest.main()
