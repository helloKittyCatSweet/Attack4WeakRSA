#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for improved partial key exposure attack demonstration
"""

import time
from coppersmith_attack import improved_coppersmith_attack
from rsa_generator import generate_small_rsa_params


def improved_attack(bit_length: int = 20, r: int = 2, s: int = 1,
                    delta: float = 0.7, exposure_type: str = "MSB") -> bool:
    """
    Improved attack workflow
    """
    print("=" * 80)
    print("Improved Partial Key Exposure Attack")
    print("=" * 80)

    try:
        # Use small parameters to ensure success
        N, e, d, p, q, phi = generate_small_rsa_params(bit_length, r, s)

        # Create partial key exposure
        d_bits = d.bit_length()
        known_bits = int(d_bits * delta)

        if exposure_type == "MSB":
            shift = d_bits - known_bits
            d0 = (d >> shift) << shift
            x_true = d - d0
            X = 2 ** shift
        else:  # LSB
            mask = (1 << known_bits) - 1
            d0 = d & mask
            x_true = (d - d0) >> known_bits
            X = 2 ** (d_bits - known_bits)

        print(f"\n[*] Exposure Settings")
        print(f"    d0 (known) = {d0}")
        print(f"    x_true (unknown) = {x_true}")
        print(f"    X (upper bound) = {X}")
        print(f"    Verification: d0 + x = {d0 + x_true} == {d} {'✓' if d0 + x_true == d else '✗'}")

        # Execute attack
        M = phi  # Use φ(N) as modulus

        # Adjust parameters based on problem size
        if bit_length <= 20:
            m, t = 2, 1
        elif bit_length <= 30:
            m, t = 3, 2
        else:
            m, t = 4, 2

        x_recovered = improved_coppersmith_attack(N, e, d0, X, M, m, t)

        # Verify results
        print("\n" + "=" * 80)
        print("Attack Results")
        print("=" * 80)

        if x_recovered is not None:
            if exposure_type == "MSB":
                d_recovered = d0 + x_recovered
            else:  # LSB
                d_recovered = (x_recovered << known_bits) + d0

            print(f"✓ Attack successful!")
            print(f"  True x = {x_true}")
            print(f"  Recovered x = {x_recovered}")
            print(f"  True d = {d}")
            print(f"  Recovered d = {d_recovered}")
            print(f"  Match = {d == d_recovered}")

            # Simple verification
            test_msg = 42
            cipher = pow(test_msg, e, N)
            decrypted = pow(cipher, d_recovered, N)
            print(f"  Test: encrypt/decrypt {'✓' if test_msg == decrypted else '✗'}")

            return True
        else:
            print("✗ Attack failed")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_demonstration():
    """
    Run the complete demonstration
    """
    print("\n" + "=" * 80)
    print("Improved Partial Key Exposure Attack Demonstration")
    print("=" * 80)

    # Test different configurations
    test_cases = [
        (16, 2, 1, 0.7, "MSB", "Small parameters, high exposure"),
        (18, 2, 1, 0.6, "MSB", "Medium parameters"),
        (16, 1, 1, 0.7, "MSB", "Standard RSA"),
    ]

    results = []

    for bit_len, r, s, delta, exp_type, desc in test_cases:
        print(f"\n[*] Test: {desc}")
        print(f"    Parameters: {bit_len}-bit primes, r={r}, s={s}, δ={delta}, {exp_type}")

        success = improved_attack(bit_len, r, s, delta, exp_type)
        results.append((desc, success))

        if not success:
            print("    ⚠ This configuration failed, trying next...")

    # Summary of results
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)

    success_count = 0
    for desc, success in results:
        status = "✓ Success" if success else "✗ Failed"
        print(f"    {status}: {desc}")
        if success:
            success_count += 1

    print(f"\n    Total success rate: {success_count}/{len(results)} ({success_count / len(results) * 100:.1f}%)")
    print("=" * 80)


if __name__ == "__main__":
    run_demonstration()