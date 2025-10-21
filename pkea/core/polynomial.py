#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polynomial class for lattice-based cryptography

Pure algorithm implementation with no I/O operations.
"""

from typing import List


class Polynomial:
    """
    Polynomial class for cryptographic operations
    
    Represents a polynomial with integer coefficients.
    Supports evaluation, multiplication, and exponentiation.
    """

    def __init__(self, coeffs: List[int]):
        """
        Initialize polynomial with coefficients
        
        Args:
            coeffs: List of coefficients [a0, a1, a2, ...] representing a0 + a1*x + a2*x^2 + ...
        """
        self.coeffs = coeffs
        self.degree = len(coeffs) - 1 if coeffs else -1

    def evaluate(self, x: int) -> int:
        """
        Evaluate polynomial at point x
        
        Args:
            x: Point to evaluate at
            
        Returns:
            Value of polynomial at x
        """
        result = 0
        for i, coeff in enumerate(self.coeffs):
            result += coeff * (x ** i)
        return result

    def __mul__(self, other):
        """
        Polynomial multiplication
        
        Args:
            other: Another Polynomial or an integer scalar
            
        Returns:
            Product polynomial
        """
        if isinstance(other, int):
            return Polynomial([coeff * other for coeff in self.coeffs])

        result_degree = self.degree + other.degree
        result_coeffs = [0] * (result_degree + 1)

        for i, coeff1 in enumerate(self.coeffs):
            for j, coeff2 in enumerate(other.coeffs):
                result_coeffs[i + j] += coeff1 * coeff2

        return Polynomial(result_coeffs)

    def __pow__(self, exponent: int):
        """
        Polynomial exponentiation
        
        Args:
            exponent: Non-negative integer exponent
            
        Returns:
            Polynomial raised to the power
        """
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
    
    def __repr__(self):
        """Developer-friendly representation"""
        return f"Polynomial({self.coeffs})"

