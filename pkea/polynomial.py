#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polynomial class for lattice-based cryptography
"""

from typing import List


class Polynomial:
    """Polynomial class for cryptographic operations"""

    def __init__(self, coeffs: List[int]):
        self.coeffs = coeffs
        self.degree = len(coeffs) - 1 if coeffs else -1

    def evaluate(self, x: int) -> int:
        """Evaluate polynomial at point x"""
        result = 0
        for i, coeff in enumerate(self.coeffs):
            result += coeff * (x ** i)
        return result

    def __mul__(self, other):
        """Polynomial multiplication"""
        if isinstance(other, int):
            return Polynomial([coeff * other for coeff in self.coeffs])

        result_degree = self.degree + other.degree
        result_coeffs = [0] * (result_degree + 1)

        for i, coeff1 in enumerate(self.coeffs):
            for j, coeff2 in enumerate(other.coeffs):
                result_coeffs[i + j] += coeff1 * coeff2

        return Polynomial(result_coeffs)

    def __pow__(self, exponent: int):
        """Polynomial exponentiation"""
        if exponent == 0:
            return Polynomial([1])
        result = Polynomial([1])
        for _ in range(exponent):
            result = result * self
        return result

    def __str__(self):
        """String representation of polynomial"""
        terms = []
        for i, coeff in enumerate(self.coeffs):
            if coeff != 0:
                if i == 0:
                    terms.append(str(coeff))
                elif i == 1:
                    terms.append(f"{coeff}x")
                else:
                    terms.append(f"{coeff}x^{i}")
        return " + ".join(terms) if terms else "0"