#!/usr/bin/env python3
"""
Common Modulus Attack on RSA

Attack Principle:
When the same message M is encrypted with the same modulus N but different public exponents e1, e2,
if gcd(e1, e2) = 1, the attacker can recover plaintext M without knowing the private key.

Mathematical Basis:
1. C1 = M^e1 mod N
2. C2 = M^e2 mod N
3. Use Extended Euclidean Algorithm to solve: e1*x + e2*y = 1
4. Compute: M = C1^x * C2^y mod N
"""

try:
    from .extended_gcd import extended_gcd
except ImportError:
    from extended_gcd import extended_gcd

import time


class CommonModulusAttack:
    """Common modulus attack on RSA"""

    def __init__(self):
        self.name = "Common Modulus Attack (RSA)"

    def attack(self, N, e1, e2, C1, C2, verbose=False):
        """
        Execute common modulus attack

        Args:
            N: RSA modulus
            e1: First public exponent
            e2: Second public exponent
            C1: Ciphertext encrypted with e1
            C2: Ciphertext encrypted with e2
            verbose: Whether to show detailed process

        Returns:
            M: Recovered plaintext, None if attack fails
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"Common Modulus Attack - RSA")
            print(f"{'='*70}")
            print(f"\n[1] Parameters:")
            print(f"  N  = {N}")
            print(f"  e1 = {e1}")
            print(f"  e2 = {e2}")
            print(f"  C1 = {C1}")
            print(f"  C2 = {C2}")

        # Step 1: Check gcd(e1, e2) = 1
        if verbose:
            print(f"\n[2] Check condition: gcd(e1, e2) = 1")

        gcd, x, y = extended_gcd(e1, e2)

        if verbose:
            print(f"  gcd({e1}, {e2}) = {gcd}")

        if gcd != 1:
            if verbose:
                print(f"  ✗ Attack failed: e1 and e2 are not coprime")
            return None

        if verbose:
            print(f"  ✓ e1 and e2 are coprime, can attack")
            print(f"\n[3] Extended Euclidean Algorithm result:")
            print(f"  {e1} × {x} + {e2} × {y} = {gcd}")
            print(f"  x = {x}")
            print(f"  y = {y}")

        # Step 2: Compute M = C1^x * C2^y mod N
        if verbose:
            print(f"\n[4] Compute plaintext:")
            print(f"  M = C1^x × C2^y mod N")

        start = time.perf_counter()

        # Handle negative exponents
        if x < 0:
            C1_inv = self._mod_inverse(C1, N)
            if C1_inv is None:
                if verbose:
                    print(f"  ✗ Cannot compute modular inverse of C1")
                return None
            C1_part = pow(C1_inv, -x, N)
        else:
            C1_part = pow(C1, x, N)

        if y < 0:
            C2_inv = self._mod_inverse(C2, N)
            if C2_inv is None:
                if verbose:
                    print(f"  ✗ Cannot compute modular inverse of C2")
                return None
            C2_part = pow(C2_inv, -y, N)
        else:
            C2_part = pow(C2, y, N)

        M = (C1_part * C2_part) % N

        elapsed = time.perf_counter() - start

        if verbose:
            print(f"  C1^{x} mod N = {C1_part}")
            print(f"  C2^{y} mod N = {C2_part}")
            print(f"  M = {M}")
            print(f"  Time: {elapsed*1000:.3f} ms")

        return M

    def _mod_inverse(self, a, m):
        """Compute modular inverse"""
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            return None
        return x % m

    def verify(self, M, N, e1, e2, C1, C2, verbose=False):
        """
        Verify attack result

        Args:
            M: Recovered plaintext
            N: RSA modulus
            e1, e2: Public exponents
            C1, C2: Ciphertexts
            verbose: Whether to show detailed information

        Returns:
            bool: Whether verification passed
        """
        if verbose:
            print(f"\n[5] Verification:")

        # Re-encrypt to verify
        C1_check = pow(M, e1, N)
        C2_check = pow(M, e2, N)

        match1 = C1_check == C1
        match2 = C2_check == C2

        if verbose:
            print(f"  M^e1 mod N = {C1_check}")
            print(f"  C1        = {C1}")
            print(f"  Match: {'✓' if match1 else '✗'}")
            print(f"\n  M^e2 mod N = {C2_check}")
            print(f"  C2        = {C2}")
            print(f"  Match: {'✓' if match2 else '✗'}")

        return match1 and match2


if __name__ == "__main__":
    # Simple test
    print("Common Modulus Attack - RSA Basic Test")

    attacker = CommonModulusAttack()

    N = 3233
    e1 = 3
    e2 = 5
    M = 42

    C1 = pow(M, e1, N)
    C2 = pow(M, e2, N)

    recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=True)

    if recovered_M == M:
        print(f"\n✓ Attack successful! Recovered plaintext: {recovered_M}")
    else:
        print(f"\n✗ Attack failed")

