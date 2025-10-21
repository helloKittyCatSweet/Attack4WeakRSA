#!/usr/bin/env python3
"""
Demo Example: Common Modulus Attack
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Crypto.Util.number import getPrime, inverse, GCD
from core import CommonModulusAttack
import time


def run_demo(bits=512, e1=3, e2=5, message=123456789):
    """
    Run common modulus attack demo

    Args:
        bits: RSA key bit length
        e1: First public exponent
        e2: Second public exponent
        message: Plaintext message
    """
    print("\n" + "="*70)
    print("Common Modulus Attack Demo")
    print("="*70)

    print("\nScenario: Two users use the same RSA modulus N but different public exponents")
    print("          Attacker intercepts two ciphertexts of the same message")

    # Generate RSA parameters
    print(f"\n[1] Generate RSA parameters ({bits}-bit)...")
    p = getPrime(bits // 2)
    q = getPrime(bits // 2)
    N = p * q
    phi = (p - 1) * (q - 1)

    # Ensure e1, e2 are coprime with phi and not equal
    while GCD(e1, phi) != 1:
        e1 += 2

    while GCD(e2, phi) != 1 or e2 == e1:
        e2 += 2

    print(f"  N = {N}")
    print(f"  N bit length: {N.bit_length()}")
    print(f"  e1 = {e1}")
    print(f"  e2 = {e2}")

    # Original message
    M = message
    print(f"\n[2] Original message:")
    print(f"  M = {M}")

    # Generate two ciphertexts
    print(f"\n[3] User 1 encrypts with e1, User 2 encrypts with e2:")
    C1 = pow(M, e1, N)
    C2 = pow(M, e2, N)
    print(f"  C1 = M^{e1} mod N = {C1}")
    print(f"  C2 = M^{e2} mod N = {C2}")

    # Execute attack
    print(f"\n[4] Attacker executes common modulus attack...")
    attacker = CommonModulusAttack()

    start = time.perf_counter()
    recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=True)
    elapsed = time.perf_counter() - start

    # Verify
    print(f"\n[5] Attack result:")
    if recovered_M == M:
        print(f"  ✓ Attack successful!")
        print(f"  Original message: {M}")
        print(f"  Recovered message: {recovered_M}")
        print(f"  Total time: {elapsed*1000:.3f} ms")
        return True
    else:
        print(f"  ✗ Attack failed")
        return False


def run_test_suite():
    """Run test suite"""
    print("\n" + "="*70)
    print("Common Modulus Attack Test Suite")
    print("="*70)

    test_cases = [
        ("Small RSA (512-bit)", 512, 3, 5),
        ("Medium RSA (1024-bit)", 1024, 7, 11),
        ("Large RSA (2048-bit)", 2048, 17, 257),
    ]

    results = []

    for name, bits, e1, e2 in test_cases:
        print(f"\n{'='*70}")
        print(f"Test: {name}")
        print(f"{'='*70}")

        # Generate parameters
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)
        N = p * q
        phi = (p - 1) * (q - 1)

        # Ensure e1, e2 are coprime with phi
        while GCD(e1, phi) != 1:
            e1 += 2
        while GCD(e2, phi) != 1 or e2 == e1:
            e2 += 2

        M = 123456789
        C1 = pow(M, e1, N)
        C2 = pow(M, e2, N)

        # Attack
        attacker = CommonModulusAttack()
        start = time.perf_counter()
        recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=False)
        elapsed = time.perf_counter() - start

        success = (recovered_M == M)
        results.append((name, success, elapsed * 1000))

        status = "✓ Success" if success else "✗ Failed"
        print(f"  Result: {status}")
        print(f"  Time: {elapsed*1000:.3f} ms")

    # Summary
    print(f"\n{'='*70}")
    print("Test Summary")
    print(f"{'='*70}")
    print(f"\n{'Test case':<30} {'Result':<10} {'Time(ms)':<10}")
    print("-" * 70)

    for name, success, elapsed in results:
        status = "✓ Success" if success else "✗ Failed"
        print(f"{name:<30} {status:<10} {elapsed:.3f}")

    success_count = sum(1 for _, s, _ in results if s)
    total_count = len(results)
    print(f"\nPass rate: {success_count}/{total_count} ({success_count*100//total_count}%)")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Common Modulus Attack Demo')
    parser.add_argument('--mode', choices=['demo', 'test'], default='demo',
                        help='Run mode: demo or test (Default: demo)')
    parser.add_argument('--bits', type=int, default=512,
                        help='RSA key bit length (Default: 512)')
    parser.add_argument('--e1', type=int, default=3,
                        help='First public exponent (Default: 3)')
    parser.add_argument('--e2', type=int, default=5,
                        help='Second public exponent (Default: 5)')
    parser.add_argument('--message', type=int, default=123456789,
                        help='Plaintext message (Default: 123456789)')
    
    args = parser.parse_args()
    
    if args.mode == 'demo':
        run_demo(args.bits, args.e1, args.e2, args.message)
    elif args.mode == 'test':
        run_test_suite()

