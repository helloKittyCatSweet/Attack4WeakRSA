"""
Continued Fraction implementation for Wiener attack

Pure algorithm with no I/O operations.
"""

from typing import List, Tuple


class ContinuedFraction:
    """Continued fraction expansion and convergent computation"""
    
    @staticmethod
    def compute_convergents(e: int, n: int) -> List[Tuple[int, int]]:
        """
        Compute convergents of continued fraction expansion of e/n
        
        Args:
            e: Public exponent
            n: RSA modulus
            
        Returns:
            List of (k, d) tuples where k/d approximates e/n
        """
        convergents = []
        
        # Initialize continued fraction expansion
        quotients = []
        a, b = e, n
        
        # Euclidean algorithm to compute continued fraction coefficients
        while b != 0:
            q = a // b
            quotients.append(q)
            a, b = b, a - q * b
        
        # Compute convergents from coefficients
        h_prev2, h_prev1 = 0, 1
        k_prev2, k_prev1 = 1, 0
        
        for q in quotients:
            h = q * h_prev1 + h_prev2
            k = q * k_prev1 + k_prev2
            
            convergents.append((h, k))
            
            h_prev2, h_prev1 = h_prev1, h
            k_prev2, k_prev1 = k_prev1, k
        
        return convergents
    
    @staticmethod
    def rational_to_contfrac(x: int, y: int) -> List[int]:
        """
        Convert rational number x/y to continued fraction representation
        
        Args:
            x: Numerator
            y: Denominator
            
        Returns:
            List of continued fraction coefficients [a0, a1, a2, ...]
        """
        quotients = []
        
        while y != 0:
            q = x // y
            quotients.append(q)
            x, y = y, x - q * y
        
        return quotients
    
    @staticmethod
    def contfrac_to_rational(coeffs: List[int]) -> Tuple[int, int]:
        """
        Convert continued fraction to rational number
        
        Args:
            coeffs: List of continued fraction coefficients
            
        Returns:
            (numerator, denominator) tuple
        """
        if not coeffs:
            return 0, 1
        
        h_prev2, h_prev1 = 0, 1
        k_prev2, k_prev1 = 1, 0
        
        for q in coeffs:
            h = q * h_prev1 + h_prev2
            k = q * k_prev1 + k_prev2
            
            h_prev2, h_prev1 = h_prev1, h
            k_prev2, k_prev1 = k_prev1, k
        
        return h_prev1, k_prev1

