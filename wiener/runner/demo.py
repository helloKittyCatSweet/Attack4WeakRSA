"""
Wiener Attack Demonstration

Handles all user interactions and demonstrations.
"""

import time
from typing import Dict, Any, Tuple
from Crypto.Util.number import getPrime, inverse, GCD

# Handle both direct and module execution
try:
    from core import WienerAttack, BunderTonienAttack, NewBoundaryAttack, WeakRSAGenerator
    from runner.visualizer import (
        print_header, print_section, print_key_info,
        print_boundary_comparison, print_attack_result, print_comparison_table
    )
except ImportError:
    from ..core import WienerAttack, BunderTonienAttack, NewBoundaryAttack, WeakRSAGenerator
    from .visualizer import (
        print_header, print_section, print_key_info,
        print_boundary_comparison, print_attack_result, print_comparison_table
    )


def run_single_attack(n: int, e: int, d: int, attack_type: str = "wiener") -> Tuple[bool, float]:
    """
    Run single attack
    
    Args:
        n: RSA modulus
        e: Public exponent
        d: Private key (for verification)
        attack_type: "wiener", "bunder_tonien", or "new_boundary"
        
    Returns:
        (success, time_ms): Success status and time in milliseconds
    """
    # Select attack method
    if attack_type == "wiener":
        attack = WienerAttack()
    elif attack_type == "bunder_tonien":
        attack = BunderTonienAttack()
    elif attack_type == "new_boundary":
        attack = NewBoundaryAttack()
    else:
        raise ValueError(f"Unknown attack type: {attack_type}")
    
    # Execute attack
    start = time.perf_counter()
    recovered_d = attack.attack(e, n)
    elapsed = time.perf_counter() - start
    
    success = (recovered_d == d)
    time_ms = elapsed * 1000
    
    # Print result
    print_attack_result(attack_type, success, d, recovered_d, time_ms)
    
    return success, time_ms


def run_comparison(n: int, e: int, d: int) -> Dict[str, Any]:
    """
    Run all three attack methods and compare
    
    Args:
        n: RSA modulus
        e: Public exponent
        d: Private key (for verification)
        
    Returns:
        Dictionary with results for each method
    """
    print_header("Attack Method Comparison")
    
    # Print key info
    print_section("RSA Parameters")
    print_key_info(n, e, d)
    
    # Print boundary comparison
    print_section("Boundary Comparison")
    print_boundary_comparison(n, d)
    
    # Run all attacks
    print_section("Attack Results")
    
    wiener = WienerAttack()
    bunder_tonien = BunderTonienAttack()
    new_boundary = NewBoundaryAttack()
    
    results = {}
    
    # Wiener attack
    start = time.perf_counter()
    d_wiener = wiener.attack(e, n)
    time_wiener = time.perf_counter() - start
    results["Wiener"] = {
        "success": d_wiener == d,
        "d": d_wiener,
        "time": time_wiener,
        "boundary": wiener.get_boundary(n)
    }
    
    # Bunder-Tonien attack
    start = time.perf_counter()
    d_bt = bunder_tonien.attack(e, n)
    time_bt = time.perf_counter() - start
    results["Bunder-Tonien"] = {
        "success": d_bt == d,
        "d": d_bt,
        "time": time_bt,
        "boundary": bunder_tonien.get_boundary(n)
    }
    
    # New boundary attack
    start = time.perf_counter()
    d_new = new_boundary.attack(e, n)
    time_new = time.perf_counter() - start
    results["New Boundary"] = {
        "success": d_new == d,
        "d": d_new,
        "time": time_new,
        "boundary": new_boundary.get_boundary(n)
    }
    
    # Print comparison table
    print_comparison_table(results)
    
    # Summary
    print("\nSummary:")
    for method, result in results.items():
        status = "✓ Success" if result["success"] else "✗ Failed"
        print(f"  {method:<20} {status}")
    
    return results


def run_demonstration():
    """Run complete demonstration"""
    print_header("Wiener Attack Comprehensive Demonstration")
    
    print("\nThis demonstration showcases three Wiener attack variants:")
    print("  1. Original Wiener Attack (1990)")
    print("  2. Bunder-Tonien Attack (2017)")
    print("  3. New Boundary Attack (2023)")
    
    # Demo 1: Basic attack with very small d
    print_header("Demo 1: Basic Wiener Attack")
    
    print("\nGenerating vulnerable RSA key...")
    print("Strategy: Using very small private key d")
    
    # Generate key
    p = getPrime(256)
    q = getPrime(256)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Use small d
    d = 12345
    while GCD(d, phi) != 1:
        d += 2
    
    e = inverse(d, phi)
    
    print(f"\nRSA Parameters:")
    print(f"  N bit length: {n.bit_length()}")
    print(f"  d = {d} ({d.bit_length()} bits)")
    print(f"  e = {e}")
    
    # Check boundary
    wiener = WienerAttack()
    wiener_bound = wiener.get_boundary(n)
    print(f"\nWiener boundary: {wiener_bound:.2e}")
    print(f"d < boundary: {'✓' if d < wiener_bound else '✗'}")
    
    # Execute attack
    print("\nExecuting Wiener attack...")
    start = time.perf_counter()
    recovered_d = wiener.attack(e, n)
    elapsed = time.perf_counter() - start
    
    # Display result
    if recovered_d == d:
        print(f"✓ Attack successful! Time: {elapsed*1000:.3f} ms")
        print(f"  Recovered private key: {recovered_d}")
        
        # Verify encryption/decryption
        msg = 123456789
        cipher = pow(msg, e, n)
        decrypted = pow(cipher, recovered_d, n)
        print(f"  Encryption/decryption verification: {'✓' if decrypted == msg else '✗'}")
    else:
        print(f"✗ Attack failed")
    
    # Demo 2: Boundary comparison
    print_header("Demo 2: Boundary Comparison")
    
    print("\nAccording to the paper, the three attack methods have the following boundaries:")
    print("  1. Wiener (1990):        d < N^0.25 / 3")
    print("  2. Bunder-Tonien (2017): d < 2√(2N)")
    print("  3. New Boundary (2023):  d < √(8.24264N)")
    
    # Test different N sizes
    test_sizes = [256, 512, 1024]

    print(f"\n{'N Bits':<10} {'Wiener (bits)':<20} {'Bunder-Tonien (bits)':<25} {'New Boundary (bits)':<25}")
    print("-" * 85)

    for bits in test_sizes:
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)
        n = p * q

        w_attack = WienerAttack()
        bt_attack = BunderTonienAttack()
        new_attack = NewBoundaryAttack()

        w_bound = w_attack.get_boundary(n)
        bt_bound = bt_attack.get_boundary(n)
        new_bound = new_attack.get_boundary(n)

        # Print bit lengths instead of values to avoid overflow
        w_bits = w_bound.bit_length() if w_bound > 0 else 0
        bt_bits = bt_bound.bit_length() if bt_bound > 0 else 0
        new_bits = new_bound.bit_length() if new_bound > 0 else 0

        print(f"{n.bit_length():<10} {w_bits:<20} {bt_bits:<25} {new_bits:<25}")
    
    print("\nKey Observations:")
    print("  • Bunder-Tonien's boundary is much larger than Wiener's")
    print("  • New Boundary's boundary is slightly larger than Bunder-Tonien's")
    print("  • All boundaries grow with N, but at different rates")
    
    # Demo 3: Attack comparison - All methods succeed
    print_header("Demo 3: Attack Comparison - All Methods Succeed")

    print("\nGenerating weak RSA key with very small d...")
    print("Strategy: d_ratio=0.24 ensures d < Wiener boundary")
    generator = WeakRSAGenerator()
    n, e, d, p, q = generator.generate_weak_rsa(bits=512, d_ratio=0.24)

    print(f"\nGenerated RSA key:")
    print(f"  N: {n.bit_length()} bits")
    print(f"  d: {d.bit_length()} bits")

    # Run comparison
    results1 = run_comparison(n, e, d)

    # Demo 4: Attack comparison - Show theoretical boundaries
    print_header("Demo 4: Attack Comparison - Demonstrating Boundaries")

    print("\nGenerating weak RSA key with medium-sized d...")
    print("Strategy: d_ratio=0.25 makes d slightly larger than Wiener boundary")
    print("Expected: Wiener fails, but Bunder-Tonien and New Boundary succeed")
    n2, e2, d2, p2, q2 = generator.generate_weak_rsa(bits=512, d_ratio=0.25)

    print(f"\nGenerated RSA key:")
    print(f"  N: {n2.bit_length()} bits")
    print(f"  d: {d2.bit_length()} bits")

    # Run comparison
    results2 = run_comparison(n2, e2, d2)

    # Summary of both demos
    print_header("Summary: Theoretical Boundaries in Action")

    print("\nDemo 3 Results (d_ratio=0.24, very small d):")
    for method, result in results1.items():
        status = "✓ Success" if result["success"] else "✗ Failed"
        print(f"  {method:<20} {status}")

    print("\nDemo 4 Results (d_ratio=0.25, medium d):")
    for method, result in results2.items():
        status = "✓ Success" if result["success"] else "✗ Failed"
        print(f"  {method:<20} {status}")

    print("\nKey Insight:")
    print("  • When d is very small (< 126 bits): All three methods succeed")
    print("  • When d is medium (128 bits): Only improved methods succeed")
    print("  • This demonstrates the theoretical improvements:")
    print("    - Bunder-Tonien (2017) relaxed Wiener's boundary")
    print("    - New Boundary (2023) further improved the boundary")
    
    print("\n" + "="*70)
    print("Demonstration Complete!")
    print("="*70)

