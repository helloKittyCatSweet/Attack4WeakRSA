#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coppersmith method implementation for partial key exposure attack

Pure algorithm implementation with no I/O operations.
"""

import math
from typing import List, Optional
from .polynomial import Polynomial
from .lll_algorithm import ImprovedLLL


def improved_coppersmith_attack(N: int, e: int, d0: int, X: int, M: int,
                                m: int = 3, t: int = 2) -> Optional[int]:
    """
    Improved Coppersmith attack for partial key exposure
    
    Uses lattice reduction to find small roots of polynomial modulo M.
    Given partial knowledge of private key d = d0 + x where |x| < X,
    recovers the unknown part x.
    
    Args:
        N: RSA modulus
        e: Public exponent
        d0: Known part of private key
        X: Upper bound on unknown part |x|
        M: Modulus for polynomial (typically φ(N))
        m: Lattice dimension parameter (higher = better but slower)
        t: Extra shift parameter (higher = better but slower)
        
    Returns:
        Recovered unknown part x, or None if attack fails
        
    Algorithm:
        1. Construct polynomial f(x) = e*x + (e*d0 - 1) mod M
        2. Build lattice from polynomial shifts
        3. Apply LLL reduction to find short vectors
        4. Extract and test roots from short vectors
    """
    # Construct base polynomial f(x) = e*x + (e*d0 - 1) mod M
    f_coeffs = [e * d0 - 1, e]  # [constant term, x coefficient]
    f_poly = Polynomial(f_coeffs)

    # Construct lattice basis polynomials
    polynomials = []

    # Use simpler construction strategy
    for j in range(m + 1):
        for i in range(m + 1):
            if i + j <= m + t:
                # g_{i,j} = x^i * f(x)^j * M^(m-j)
                poly = Polynomial([1])  # Initialize to 1

                # x^i
                if i > 0:
                    x_poly = Polynomial([0] * i + [1])  # x^i
                    poly = poly * x_poly

                # f(x)^j
                if j > 0:
                    poly = poly * (f_poly ** j)

                # M^(m-j)
                if m - j > 0:
                    poly = poly * (M ** (m - j))

                polynomials.append(poly)

    # Build lattice basis matrix
    max_degree = max(poly.degree for poly in polynomials)
    lattice_dim = len(polynomials)

    # Create matrix
    lattice_matrix = []
    for poly in polynomials:
        row = [0] * lattice_dim
        for deg, coeff in enumerate(poly.coeffs):
            if deg < lattice_dim:
                # Scale: multiply by X^deg
                row[deg] = coeff * (X ** deg)
        lattice_matrix.append(row)

    # Perform LLL reduction
    lll = ImprovedLLL(delta=0.99)
    reduced_lattice = lll.reduce(lattice_matrix)

    # Analyze results - calculate norms of all vectors
    vector_norms = []
    for i, row in enumerate(reduced_lattice):
        norm = math.sqrt(sum(x * x for x in row))
        vector_norms.append((i, norm, row))

    # Sort by norm
    vector_norms.sort(key=lambda x: x[1])

    # Check first few short vectors
    for idx, (i, norm, vector) in enumerate(vector_norms[:10]):
        # Reconstruct polynomial
        poly_coeffs = []
        for deg in range(len(vector)):
            # Unscale: divide by X^deg
            if X ** deg != 0:
                coeff = vector[deg] // (X ** deg)
            else:
                coeff = vector[deg]
            poly_coeffs.append(coeff)

        # Find integer roots - test positive values
        for test_x in range(0, min(X, 10000)):  # Limit search range
            value = 0
            for deg, coeff in enumerate(poly_coeffs):
                value += coeff * (test_x ** deg)

            if value == 0 and 0 < test_x < X:
                # Verify
                if (e * (d0 + test_x) - 1) % M == 0:
                    return test_x

        # Also test negative roots
        for test_x in range(-min(X, 10000), 0):
            value = 0
            for deg, coeff in enumerate(poly_coeffs):
                value += coeff * (test_x ** deg)

            if value == 0 and -X < test_x < 0:
                # Verify
                if (e * (d0 + test_x) - 1) % M == 0:
                    return test_x

    # No valid root found
    return None

