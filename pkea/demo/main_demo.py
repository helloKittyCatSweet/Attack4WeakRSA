#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main demonstration entry point for RSA Partial Key Exposure Attack

Provides high-level interface for running attacks and demonstrations.
"""

from typing import List, Tuple

# Handle both direct and module execution
try:
    from core import generate_small_rsa_params
    from attack import PartialKeyExposureAttack, simulate_exposure, ExposureType
    from attack.partial_key_attack import AttackConfig
    from config import RSAConfig, ExperimentConfig
except ImportError:
    from ..core import generate_small_rsa_params
    from ..attack import PartialKeyExposureAttack, simulate_exposure, ExposureType
    from ..attack.partial_key_attack import AttackConfig
    from ..config import RSAConfig, ExperimentConfig


def run_single_attack(
    rsa_config: RSAConfig,
    exp_config: ExperimentConfig,
    verbose: bool = True
) -> bool:
    """
    Run a single attack with given configuration

    Args:
        rsa_config: RSA parameter configuration
        exp_config: Experiment configuration
        verbose: Whether to print detailed output

    Returns:
        True if attack succeeded, False otherwise
    """
    if verbose:
        print("=" * 80)
        print("RSA Partial Key Exposure Attack")
        print("=" * 80)
        print(f"RSA Config: {rsa_config.bit_length}-bit primes, r={rsa_config.r}, s={rsa_config.s}")
        print(f"Experiment: {exp_config.description}")
        print(f"Exposure: {exp_config.delta*100:.0f}% {exp_config.exposure_type}")
        print("=" * 80)
    
    try:
        # Generate RSA parameters
        N, e, d, p, q, phi = generate_small_rsa_params(
            rsa_config.bit_length, rsa_config.r, rsa_config.s
        )

        if verbose:
            print(f"\n[*] Generated RSA Parameters")
            print(f"    p = {p}")
            print(f"    q = {q}")
            print(f"    N = {N}")
            print(f"    e = {e}")
            print(f"    d = {d}")
            print(f"    d bit length = {d.bit_length()} bits")

        # Simulate exposure
        exposure = simulate_exposure(d, exp_config.delta, exp_config.exposure_type)

        if verbose:
            print(f"\n[*] Exposure Simulation")
            print(f"    Type: {exposure.exposure_type.value}")
            print(f"    Known bits: {exposure.known_bits}")
            print(f"    Unknown bits: {exposure.unknown_bits}")
            print(f"    d0 (known) = {exposure.d0}")
            print(f"    x_true (unknown) = {exposure.x_true}")
            print(f"    X (upper bound) = {exposure.X}")
            print(f"    Verification: d0 + x = {exposure.d0 + exposure.x_true} == {d} {'✓' if exposure.verify_reconstruction(d) else '✗'}")

        # Setup attack
        attack_config = AttackConfig(m=exp_config.m, t=exp_config.t)
        attack = PartialKeyExposureAttack(N, e, phi, exposure.d0, exposure.X, attack_config)

        if verbose:
            print(f"\n[*] Executing Attack")
            print(f"    Parameters: m={exp_config.m}, t={exp_config.t}")
        
        # Run attack with verification
        attack_result, verification = attack.run_with_verification(
            d, exposure.exposure_type, exposure.known_bits
        )

        # Display results
        if verbose:
            print(f"\n" + "=" * 80)
            print("Attack Results")
            print("=" * 80)

        if attack_result.success:
            if verbose:
                print(f"✓ Attack successful!")
                print(f"  Time: {attack_result.elapsed_time:.3f} seconds")
                print(f"  True x = {exposure.x_true}")
                print(f"  Recovered x = {attack_result.x_recovered}")
                print(f"  True d = {d}")
                print(f"  Recovered d = {attack_result.d_recovered}")
                print(f"  Match = {d == attack_result.d_recovered}")

                if verification:
                    print(f"\n[*] Verification")
                    print(f"    {verification.details}")

            return True
        else:
            if verbose:
                print(f"✗ Attack failed")
                print(f"  Time: {attack_result.elapsed_time:.3f} seconds")
                print(f"  Details: {attack_result.details}")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_demonstration():
    """
    Run complete demonstration with multiple test cases
    """
    print("\n" + "=" * 80)
    print("RSA Partial Key Exposure Attack - Complete Demonstration")
    print("=" * 80)
    
    # Define test cases
    test_cases: List[Tuple[RSAConfig, ExperimentConfig, str]] = [
        (
            RSAConfig(bit_length=16, r=2, s=1),
            ExperimentConfig(delta=0.75, exposure_type="MSB", m=3, t=2),
            "Small parameters, high exposure (75% MSB)"
        ),
        (
            RSAConfig(bit_length=18, r=2, s=1),
            ExperimentConfig(delta=0.65, exposure_type="MSB", m=4, t=2),
            "Medium parameters, balanced (65% MSB)"
        ),
        (
            RSAConfig(bit_length=16, r=1, s=1),
            ExperimentConfig(delta=0.75, exposure_type="MSB", m=3, t=1),
            "Standard RSA (r=1, s=1)"
        ),
    ]
    
    results = []

    for rsa_config, exp_config, desc in test_cases:
        print(f"\n[*] Test: {desc}")

        success = run_single_attack(rsa_config, exp_config, verbose=True)
        results.append((desc, success))

        if not success:
            print("    ⚠ This configuration failed, trying next...")

    # Summary
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

