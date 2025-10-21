#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification module for attack results

Verifies correctness of recovered private keys.
"""

from typing import Tuple
from dataclasses import dataclass


@dataclass
class VerificationResult:
    """
    Result of verification
    
    Attributes:
        success: Whether verification succeeded
        key_match: Whether recovered key matches original
        encryption_works: Whether encryption/decryption works
        details: Additional details
    """
    success: bool
    key_match: bool
    encryption_works: bool
    details: str = ""


def verify_private_key(d_true: int, d_recovered: int, e: int, N: int, M: int) -> VerificationResult:
    """
    Verify that recovered private key is correct
    
    Checks:
    1. d_recovered == d_true (direct match)
    2. (e * d_recovered - 1) % M == 0 (mathematical correctness)
    
    Args:
        d_true: True private key
        d_recovered: Recovered private key
        e: Public exponent
        N: RSA modulus
        M: Modulus (typically φ(N))
        
    Returns:
        VerificationResult with verification status
    """
    key_match = (d_true == d_recovered)
    
    # Check mathematical correctness: e*d ≡ 1 (mod M)
    math_correct = ((e * d_recovered - 1) % M == 0)
    
    success = key_match and math_correct
    
    details = []
    if key_match:
        details.append("Key match: ✓")
    else:
        details.append(f"Key match: ✗ (true={d_true}, recovered={d_recovered})")
    
    if math_correct:
        details.append("Math check: ✓")
    else:
        details.append(f"Math check: ✗ (e*d-1 mod M = {(e * d_recovered - 1) % M})")
    
    return VerificationResult(
        success=success,
        key_match=key_match,
        encryption_works=False,  # Will be set by encryption test
        details="; ".join(details)
    )


def verify_encryption_decryption(d_recovered: int, e: int, N: int, test_message: int = 42) -> bool:
    """
    Verify that recovered key works for encryption/decryption
    
    Tests: encrypt(test_message) -> decrypt(ciphertext) == test_message
    
    Args:
        d_recovered: Recovered private key
        e: Public exponent
        N: RSA modulus
        test_message: Message to test (default: 42)
        
    Returns:
        True if encryption/decryption works correctly
    """
    try:
        # Encrypt with public key
        ciphertext = pow(test_message, e, N)
        
        # Decrypt with recovered private key
        decrypted = pow(ciphertext, d_recovered, N)
        
        return decrypted == test_message
    except Exception:
        return False


def full_verification(d_true: int, d_recovered: int, e: int, N: int, M: int) -> VerificationResult:
    """
    Perform full verification including encryption test
    
    Args:
        d_true: True private key
        d_recovered: Recovered private key
        e: Public exponent
        N: RSA modulus
        M: Modulus (typically φ(N))
        
    Returns:
        Complete VerificationResult
    """
    result = verify_private_key(d_true, d_recovered, e, N, M)
    
    # Add encryption test
    encryption_works = verify_encryption_decryption(d_recovered, e, N)
    result.encryption_works = encryption_works
    
    if encryption_works:
        result.details += "; Encryption test: ✓"
    else:
        result.details += "; Encryption test: ✗"
    
    result.success = result.success and encryption_works
    
    return result

