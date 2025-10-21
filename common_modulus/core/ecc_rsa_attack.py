#!/usr/bin/env python3
"""
Common Modulus Attack on ECC-RSA Variant

Based on paper: "Common Modulus Attack on the Elliptic Curve-Based RSA Algorithm Variant"
Authors: Boudabra & Nitaj
"""

try:
    from .extended_gcd import extended_gcd
except ImportError:
    from extended_gcd import extended_gcd

import time


class ECCRSACommonModulusAttack:
    """Common modulus attack on ECC-RSA variant"""

    def __init__(self, a, b, p):
        """
        Initialize elliptic curve parameters

        Args:
            a, b: Elliptic curve parameters y^2 = x^3 + ax + b
            p: Prime modulus
        """
        self.name = "Common Modulus Attack (ECC-RSA)"
        self.a = a
        self.b = b
        self.p = p

    def point_add(self, P, Q):
        """
        Elliptic curve point addition

        Args:
            P, Q: Points on elliptic curve (x, y) or None (point at infinity)

        Returns:
            Point P + Q on elliptic curve
        """
        if P is None:
            return Q
        if Q is None:
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        if x1 == x2:
            if y1 == y2:
                # Point doubling
                s = (3 * x1 * x1 + self.a) * pow(2 * y1, -1, self.p) % self.p
            else:
                # P + (-P) = O (point at infinity)
                return None
        else:
            # Normal point addition
            s = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p

        x3 = (s * s - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def scalar_mult(self, k, P):
        """
        Elliptic curve scalar multiplication (point doubling)

        Args:
            k: Scalar (integer)
            P: Point on elliptic curve

        Returns:
            k * P (k times point P)
        """
        if k == 0:
            return None  # Point at infinity

        if k < 0:
            # Negative multiplication: -k*P = k*(-P)
            k = -k
            P = (P[0], -P[1] % self.p)

        # Binary expansion method (double-and-add)
        result = None
        addend = P

        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1

        return result
    
    def attack(self, N, e1, e2, C1, C2):
        """
        Execute common modulus attack on ECC-RSA variant

        Args:
            N: Modulus
            e1, e2: Public exponents
            C1, C2: Ciphertext points (r, y)

        Returns:
            M: Recovered plaintext point, None if attack fails
        """
        # Check gcd(e1, e2) = 1
        gcd, x, y = extended_gcd(e1, e2)

        if gcd != 1:
            return None

        # Compute M = x*C1 + y*C2
        P1 = self.scalar_mult(x, C1)
        P2 = self.scalar_mult(y, C2)
        M = self.point_add(P1, P2)

        return M
    
    def verify_point_on_curve(self, P):
        """
        Verify if point is on elliptic curve

        Args:
            P: Point (x, y)

        Returns:
            bool: Whether point is on curve
        """
        if P is None:
            return True  # Point at infinity

        x, y = P
        lhs = (y * y) % self.p
        rhs = (x * x * x + self.a * x + self.b) % self.p

        return lhs == rhs


if __name__ == "__main__":
    # Simple test
    print("Common Modulus Attack - ECC-RSA Basic Test")

    # Elliptic curve parameters (example)
    a = 1
    b = 1
    p = 23  # Small prime for testing

    attacker = ECCRSACommonModulusAttack(a, b, p)

    # Test point addition
    P = (3, 10)
    Q = (9, 7)

    print(f"\nTest point addition:")
    print(f"  P = {P}")
    print(f"  Q = {Q}")
    print(f"  P + Q = {attacker.point_add(P, Q)}")

    # Test scalar multiplication
    print(f"\nTest scalar multiplication:")
    print(f"  2·P = {attacker.scalar_mult(2, P)}")
    print(f"  3·P = {attacker.scalar_mult(3, P)}")

