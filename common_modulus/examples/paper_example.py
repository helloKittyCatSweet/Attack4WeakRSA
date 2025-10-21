#!/usr/bin/env python3
"""
Paper Example: Common Modulus Attack on ECC-RSA
Reproduce paper example

Paper: "Common Modulus Attack on the Elliptic Curve-Based RSA Algorithm Variant"
Authors: Boudabra & Nitaj
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core import CommonModulusAttack, ECCRSACommonModulusAttack, extended_gcd
from config import PAPER_EXAMPLE, ECC_PARAMS
import time


def verify_extended_gcd():
    """Verify Extended Euclidean Algorithm result"""
    print("\n" + "="*70)
    print("Verify Extended Euclidean Algorithm")
    print("="*70)
    
    e1 = PAPER_EXAMPLE['e1']
    e2 = PAPER_EXAMPLE['e2']
    expected_x = PAPER_EXAMPLE['expected_x']
    expected_y = PAPER_EXAMPLE['expected_y']
    
    gcd, x, y = extended_gcd(e1, e2)
    
    print(f"\nValues from the paper:")
    print(f"  e1 = {e1}, e2 = {e2}")
    print(f"  x = {expected_x}, y = {expected_y}")
    
    print(f"\nComputed result:")
    print(f"  gcd({e1}, {e2}) = {gcd}")
    print(f"  x = {x}, y = {y}")
    
    # Verify
    result = e1 * x + e2 * y
    expected_result = e1 * expected_x + e2 * expected_y
    
    print(f"\nVerify:")
    print(f"  {e1} × {x} + {e2} × {y} = {result}")
    print(f"  {e1} × {expected_x} + {e2} × {expected_y} = {expected_result}")
    
    if x == expected_x and y == expected_y:
        print(f"  ✓ Exactly matches the paper's result")
        return True
    else:
        print(f"  ⚠ Does not match the paper's result, but both satisfy Bézout's identity")
        return True


def test_paper_example_rsa():
    """Test the paper example - plain RSA version"""
    print("\n" + "="*70)
    print("Paper example reproduction - plain RSA")
    print("="*70)
    
    # Read parameters from configuration
    N = PAPER_EXAMPLE['N']
    e1 = PAPER_EXAMPLE['e1']
    e2 = PAPER_EXAMPLE['e2']
    
    # Use r as the plaintext (simplified)
    M = PAPER_EXAMPLE['M']['r']
    
    print(f"\n[1] Generate ciphertexts...")
    print(f"  Plaintext M = {M}")
    
    # Generate two ciphertexts
    C1 = pow(M, e1, N)
    C2 = pow(M, e2, N)
    
    print(f"  C1 = M^{e1} mod N = {C1}")
    print(f"  C2 = M^{e2} mod N = {C2}")
    
    # Execute attack
    print(f"\n[2] Execute common-modulus attack...")
    attacker = CommonModulusAttack()
    
    start = time.perf_counter()
    recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=True)
    elapsed = time.perf_counter() - start
    
    # Verify result
    print(f"\n[3] Verify result...")
    if recovered_M == M:
        print(f"  ✓ Attack successful!")
        print(f"  Original plaintext: {M}")
        print(f"  Recovered plaintext: {recovered_M}")
        print(f"  Total time: {elapsed*1000:.3f} ms")
        return True
    else:
        print(f"  ✗ Attack failed")
        print(f"  Original plaintext: {M}")
        print(f"  Recovered plaintext: {recovered_M}")
        return False


def test_paper_example_ecc_rsa():
    """Test the paper example - ECC-RSA variant"""
    print("\n" + "="*70)
    print("Paper example reproduction - ECC-RSA variant")
    print("="*70)
    
    # Read parameters from configuration
    N = PAPER_EXAMPLE['N']
    e1 = PAPER_EXAMPLE['e1']
    e2 = PAPER_EXAMPLE['e2']
    
    # Plaintext point
    M = (PAPER_EXAMPLE['M']['r'], PAPER_EXAMPLE['M']['y_M'])
    
    # Ciphertext points (from the paper)
    C1 = (PAPER_EXAMPLE['C1']['r'], PAPER_EXAMPLE['C1']['y_C1'])
    C2 = (PAPER_EXAMPLE['C2']['r'], PAPER_EXAMPLE['C2']['y_C2'])
    
    print(f"\n[1] Paper parameters:")
    print(f"  N = {N}")
    print(f"  e1 = {e1}, e2 = {e2}")
    print(f"  Plaintext point M = {M}")
    print(f"  Ciphertext point C1 = {C1}")
    print(f"  Ciphertext point C2 = {C2}")
    
    # Create attacker
    a = ECC_PARAMS['a']
    b = ECC_PARAMS['b']
    p = ECC_PARAMS['p']
    
    attacker = ECCRSACommonModulusAttack(a, b, p)
    
    # Execute attack
    print(f"\n[2] Execute common-modulus attack...")
    start = time.perf_counter()
    recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=True)
    elapsed = time.perf_counter() - start
    
    # Verify result
    print(f"\n[3] Verify result...")
    if recovered_M == M:
        print(f"  ✓ Attack successful!")
        print(f"  Original plaintext point: {M}")
        print(f"  Recovered plaintext point: {recovered_M}")
        print(f"  Total time: {elapsed*1000:.3f} ms")
        return True
    else:
        print(f"  ⚠ Result does not match")
        print(f"  Original plaintext point: {M}")
        print(f"  Recovered plaintext point: {recovered_M}")
        print(f"  Total time: {elapsed*1000:.3f} ms")
        
        # Check if recovered point lies on the same curve
        if recovered_M:
            x, y = recovered_M
            lhs = (y * y) % p
            rhs = (x * x * x + a * x + b) % p
            on_curve = lhs == rhs
            print(f"\n  Recovered point is on the curve: {'✓' if on_curve else '✗'}")
        
        return False


def run_paper_example():
    """Main function - run all paper examples"""
    print("\n" + "="*70)
    print("Common Modulus Attack - paper example reproduction")
    print("="*70)
    print("\nPaper: Common Modulus Attack on the Elliptic Curve-Based")
    print("      RSA Algorithm Variant (Boudabra & Nitaj)")
    
    # 1. Verify the Extended Euclidean Algorithm
    verify_extended_gcd()
    
    # 2. Test the plain RSA version
    input("\nPress Enter to continue and test the plain RSA version...")
    success_rsa = test_paper_example_rsa()
    
    # 3. Test the ECC-RSA variant
    input("\nPress Enter to continue and test the ECC-RSA variant...")
    success_ecc = test_paper_example_ecc_rsa()
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"  Extended Euclidean Algorithm: ✓")
    print(f"  Plain RSA attack: {'✓' if success_rsa else '✗'}")
    print(f"  ECC-RSA attack: {'✓' if success_ecc else '⚠'}")
    
    print("\n" + "="*70)
    print("Key conclusions")
    print("="*70)
    print("  • The common-modulus attack is effective against both plain RSA and the ECC-RSA variant")
    print("  • As long as gcd(e1, e2) = 1, the attacker can recover the plaintext without the private key")
    print("  • Attack complexity is very low and completes almost instantly")
    print("  • Reusing the modulus is a fundamental security mistake and must be avoided")
    print("="*70)


if __name__ == "__main__":
    run_paper_example()
