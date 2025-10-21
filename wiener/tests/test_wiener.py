"""
Unit tests for Wiener Attack

Tests all three attack methods and key generation.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import WienerAttack, BunderTonienAttack, NewBoundaryAttack, WeakRSAGenerator
from Crypto.Util.number import getPrime, inverse, GCD


def test_wiener_attack_basic():
    """Test basic Wiener attack with very small d"""
    print("\n[Test 1] Basic Wiener Attack")
    
    # Generate key with very small d
    p = getPrime(256)
    q = getPrime(256)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    d = 12345
    while GCD(d, phi) != 1:
        d += 2
    
    e = inverse(d, phi)
    
    # Attack
    attack = WienerAttack()
    recovered_d = attack.attack(e, n)
    
    # Verify
    assert recovered_d == d, f"Expected {d}, got {recovered_d}"
    print(f"  ✓ Wiener attack successful: d={d}")


def test_bunder_tonien_attack():
    """Test Bunder-Tonien attack"""
    print("\n[Test 2] Bunder-Tonien Attack")
    
    # Generate weak key
    generator = WeakRSAGenerator()
    n, e, d, p, q = generator.generate_weak_rsa(bits=512, d_ratio=0.25)
    
    # Attack
    attack = BunderTonienAttack()
    recovered_d = attack.attack(e, n)
    
    # Verify
    assert recovered_d == d, f"Expected {d}, got {recovered_d}"
    print(f"  ✓ Bunder-Tonien attack successful: d bit length={d.bit_length()}")


def test_new_boundary_attack():
    """Test New Boundary attack"""
    print("\n[Test 3] New Boundary Attack")
    
    # Generate weak key
    generator = WeakRSAGenerator()
    n, e, d, p, q = generator.generate_weak_rsa(bits=512, d_ratio=0.25)
    
    # Attack
    attack = NewBoundaryAttack()
    recovered_d = attack.attack(e, n)
    
    # Verify
    assert recovered_d == d, f"Expected {d}, got {recovered_d}"
    print(f"  ✓ New Boundary attack successful: d bit length={d.bit_length()}")


def test_boundary_comparison():
    """Test boundary comparison"""
    print("\n[Test 4] Boundary Comparison")
    
    p = getPrime(256)
    q = getPrime(256)
    n = p * q
    
    wiener = WienerAttack()
    bunder_tonien = BunderTonienAttack()
    new_boundary = NewBoundaryAttack()
    
    w_bound = wiener.get_boundary(n)
    bt_bound = bunder_tonien.get_boundary(n)
    new_bound = new_boundary.get_boundary(n)
    
    # Verify ordering: Wiener < Bunder-Tonien <= New Boundary
    assert w_bound < bt_bound, "Wiener boundary should be smaller than Bunder-Tonien"
    assert bt_bound <= new_bound, "Bunder-Tonien boundary should be <= New Boundary"
    
    print(f"  ✓ Boundary ordering correct:")
    print(f"    Wiener: {w_bound.bit_length()} bits")
    print(f"    Bunder-Tonien: {bt_bound.bit_length()} bits")
    print(f"    New Boundary: {new_bound.bit_length()} bits")


def test_weak_key_generation():
    """Test weak key generation"""
    print("\n[Test 5] Weak Key Generation")
    
    generator = WeakRSAGenerator()
    
    # Test generate_weak_rsa
    n, e, d, p, q = generator.generate_weak_rsa(bits=512, d_ratio=0.25)
    
    # Verify RSA properties
    assert n == p * q, "n should equal p * q"
    phi = (p - 1) * (q - 1)
    assert (e * d) % phi == 1, "e * d should be 1 mod phi"
    
    # Verify d is small
    expected_d_bits = int(512 * 0.25)
    assert d.bit_length() <= expected_d_bits + 10, f"d should be around {expected_d_bits} bits"
    
    print(f"  ✓ Weak key generation successful:")
    print(f"    N: {n.bit_length()} bits")
    print(f"    d: {d.bit_length()} bits")


def test_vulnerability_check():
    """Test vulnerability checking"""
    print("\n[Test 6] Vulnerability Check")
    
    generator = WeakRSAGenerator()
    n, e, d, p, q = generator.generate_weak_rsa(bits=512, d_ratio=0.25)
    
    # Check vulnerability
    vuln_info = generator.check_vulnerability(n, d)
    
    # Verify structure
    assert 'd' in vuln_info
    assert 'wiener_vulnerable' in vuln_info
    assert 'bunder_tonien_vulnerable' in vuln_info
    assert 'new_boundary_vulnerable' in vuln_info
    
    print(f"  ✓ Vulnerability check successful:")
    print(f"    Wiener vulnerable: {vuln_info['wiener_vulnerable']}")
    print(f"    Bunder-Tonien vulnerable: {vuln_info['bunder_tonien_vulnerable']}")
    print(f"    New Boundary vulnerable: {vuln_info['new_boundary_vulnerable']}")


def test_encryption_decryption():
    """Test encryption/decryption with recovered key"""
    print("\n[Test 7] Encryption/Decryption Verification")

    # Generate key with very small d (guaranteed to work with Wiener)
    p = getPrime(256)
    q = getPrime(256)
    n = p * q
    phi = (p - 1) * (q - 1)

    d = 12345
    while GCD(d, phi) != 1:
        d += 2

    e = inverse(d, phi)

    # Attack
    attack = WienerAttack()
    recovered_d = attack.attack(e, n)

    # Verify attack succeeded
    assert recovered_d is not None, "Attack failed to recover d"
    assert recovered_d == d, f"Expected {d}, got {recovered_d}"

    # Test encryption/decryption
    msg = 123456789
    cipher = pow(msg, e, n)
    decrypted = pow(cipher, recovered_d, n)

    assert decrypted == msg, f"Decryption failed: expected {msg}, got {decrypted}"
    print(f"  ✓ Encryption/decryption successful with recovered key")


def run_all_tests():
    """Run all tests"""
    print("="*70)
    print("Running Wiener Attack Tests")
    print("="*70)
    
    tests = [
        test_wiener_attack_basic,
        test_bunder_tonien_attack,
        test_new_boundary_attack,
        test_boundary_comparison,
        test_weak_key_generation,
        test_vulnerability_check,
        test_encryption_decryption,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Test error: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

