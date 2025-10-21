"""
Wiener Attack and its improvements implementation

Pure algorithms with no I/O operations.
"""

import math
from typing import Optional, Dict, Any
from .continued_fraction import ContinuedFraction
from .math_utils import isqrt


class WienerAttack:
    """Original Wiener Attack (1990)"""
    
    def __init__(self):
        self.cf = ContinuedFraction()
    
    def attack(self, e: int, n: int, n_prime: Optional[int] = None) -> Optional[int]:
        """
        Execute Wiener attack
        
        Condition: d < N^0.25 / 3
        
        Args:
            e: Public exponent
            n: RSA modulus
            n_prime: Alternative modulus (for improved attacks)
            
        Returns:
            d: Private key (if successful), None (if failed)
        """
        # Use n_prime if provided, otherwise use n
        target_n = n_prime if n_prime is not None else n
        
        # Compute convergents of e/target_n
        convergents = self.cf.compute_convergents(e, target_n)
        
        for k, d_candidate in convergents:
            # Skip invalid values
            if k == 0 or d_candidate == 0:
                continue
            
            # Check if within theoretical boundary
            if not self._check_boundary(n, d_candidate):
                continue
            
            # Check if satisfies ed ≡ 1 (mod φ(n))
            if self._check_candidate(e, n, k, d_candidate):
                return d_candidate
        
        return None
    
    def _check_boundary(self, n: int, d: int) -> bool:
        """Check if within theoretical boundary"""
        return d < self.get_boundary(n)
    
    def _check_candidate(self, e: int, n: int, k: int, d: int) -> bool:
        """
        Check if candidate private key d is correct
        
        Verification:
        1. ed - 1 should be divisible by k
        2. Compute φ(n) = (ed - 1) / k
        3. Recover p and q from φ(n) and n
        4. Verify pq = n
        """
        # Check ed ≡ 1 (mod k)
        if (e * d - 1) % k != 0:
            return False
        
        phi = (e * d - 1) // k
        
        # Compute p and q from n and φ(n)
        # n = pq, φ(n) = (p-1)(q-1) = n - (p+q) + 1
        # Therefore: p + q = n - φ(n) + 1
        s = n - phi + 1
        
        # Solve equation: x^2 - sx + n = 0
        # p, q = (s ± sqrt(s^2 - 4n)) / 2
        discriminant = s * s - 4 * n
        
        if discriminant < 0:
            return False
        
        sqrt_d = isqrt(discriminant)
        
        # Check if perfect square
        if sqrt_d * sqrt_d != discriminant:
            return False
        
        p = (s + sqrt_d) // 2
        q = (s - sqrt_d) // 2
        
        # Verify
        return p * q == n and p > 1 and q > 1
    
    def get_boundary(self, n: int) -> int:
        """Return theoretical boundary of Wiener attack"""
        # d < N^0.25 / 3
        # Use integer arithmetic to avoid float overflow
        # N^0.25 = sqrt(sqrt(N))
        sqrt_n = isqrt(n)
        sqrt_sqrt_n = isqrt(sqrt_n)
        return sqrt_sqrt_n // 3


class BunderTonienAttack(WienerAttack):
    """Bunder-Tonien Improved Attack (2017)"""
    
    def attack(self, e: int, n: int) -> Optional[int]:
        """
        Execute Bunder-Tonien attack
        
        Condition: d < 2*sqrt(2*N)
        Uses N' instead of N for continued fraction
        """
        n_prime = self._compute_n_prime(n)
        return super().attack(e, n, n_prime)
    
    def _compute_n_prime(self, n: int) -> int:
        """
        Compute Bunder-Tonien's N'
        N' = floor(N - (1 + 3/(2√2))√N + 1)
        """
        sqrt_n = isqrt(n)
        # 1 + 3/(2√2) ≈ 1 + 1.06066 = 2.06066
        coefficient = 1 + 3 / (2 * math.sqrt(2))
        n_prime = n - int(coefficient * sqrt_n) + 1
        return max(n_prime, 1)  # Ensure positive
    
    def get_boundary(self, n: int) -> int:
        """Return theoretical boundary of Bunder-Tonien attack"""
        # d < 2 * sqrt(2 * N)
        return 2 * isqrt(2 * n)


class NewBoundaryAttack(BunderTonienAttack):
    """
    New Boundary Attack (2023)
    Based on paper: "A New Boundary of Minimum Private Key on Wiener Attack Against RSA Algorithm"
    """
    
    def attack(self, e: int, n: int) -> Optional[int]:
        """
        Execute new boundary attack
        
        Condition: d < sqrt(8.24264*N) ≈ sqrt((8 + 6*sqrt(2))*N)
        Uses same N' as Bunder-Tonien but with relaxed boundary
        """
        n_prime = self._compute_n_prime(n)
        return super().attack(e, n)
    
    def get_boundary(self, n: int) -> int:
        """
        Return theoretical boundary of new boundary attack
        
        According to paper Lemma 3.1:
        α = 8 + 6*sqrt(2) ≈ 16.4853
        d < sqrt(α/2 * N) ≈ sqrt(8.24264 * N)
        """
        # Use exact calculation to avoid floating point errors
        # sqrt(8.24264 * N) = sqrt(824264/100000 * N)
        return isqrt(824264 * n // 100000)
    
    def verify_inequality(self, n: int) -> bool:
        """
        Verify inequality from paper (Lemma 3.1)
        
        (3*sqrt(2) - 2*N + 4) / (2*N - 3*sqrt(2*N)) < 1 / (α*N)
        
        When N → ∞, left side approaches 1/(8 + 6*sqrt(2))
        """
        # For large integers, use approximate calculation
        sqrt_2 = math.sqrt(2)
        sqrt_n = math.sqrt(n)
        
        numerator = (3/sqrt_2 - 2) * sqrt_n + 4
        denominator = 2 * (n - (3/sqrt_2) * sqrt_n)
        
        if denominator <= 0:
            return False
        
        left_side = numerator / denominator
        
        alpha = 8 + 6 * sqrt_2
        right_side = 1 / (alpha * n)
        
        return left_side < right_side


class AttackComparison:
    """Attack method comparison tool"""
    
    def __init__(self):
        self.wiener = WienerAttack()
        self.bunder_tonien = BunderTonienAttack()
        self.new_boundary = NewBoundaryAttack()
    
    def compare_boundaries(self, n: int) -> Dict[str, Any]:
        """
        Compare theoretical boundaries of three attack methods
        
        Returns:
            dict: Dictionary containing various boundary values
        """
        wiener_bound = self.wiener.get_boundary(n)
        bt_bound = self.bunder_tonien.get_boundary(n)
        new_bound = self.new_boundary.get_boundary(n)
        
        return {
            "n": n,
            "n_bits": n.bit_length(),
            "wiener": {
                "boundary": wiener_bound,
                "boundary_bits": wiener_bound.bit_length() if wiener_bound > 0 else 0,
                "formula": "N^0.25 / 3"
            },
            "bunder_tonien": {
                "boundary": bt_bound,
                "boundary_bits": bt_bound.bit_length() if bt_bound > 0 else 0,
                "formula": "2*sqrt(2*N)",
                "improvement_ratio": bt_bound / wiener_bound if wiener_bound > 0 else 0
            },
            "new_boundary": {
                "boundary": new_bound,
                "boundary_bits": new_bound.bit_length() if new_bound > 0 else 0,
                "formula": "sqrt(8.24264*N)",
                "improvement_ratio": new_bound / wiener_bound if wiener_bound > 0 else 0,
                "vs_bunder_tonien": new_bound / bt_bound if bt_bound > 0 else 0
            }
        }
    
    def attack_all(self, e: int, n: int) -> Dict[str, Any]:
        """
        Attempt attack using all three methods
        
        Returns:
            dict: Dictionary containing attack results and timing
        """
        import time
        
        results = {}
        
        # Wiener attack
        start = time.perf_counter()
        d_wiener = self.wiener.attack(e, n)
        time_wiener = time.perf_counter() - start
        results["wiener"] = {
            "success": d_wiener is not None,
            "d": d_wiener,
            "time": time_wiener,
            "boundary": self.wiener.get_boundary(n)
        }
        
        # Bunder-Tonien attack
        start = time.perf_counter()
        d_bt = self.bunder_tonien.attack(e, n)
        time_bt = time.perf_counter() - start
        results["bunder_tonien"] = {
            "success": d_bt is not None,
            "d": d_bt,
            "time": time_bt,
            "boundary": self.bunder_tonien.get_boundary(n)
        }
        
        # New boundary attack
        start = time.perf_counter()
        d_new = self.new_boundary.attack(e, n)
        time_new = time.perf_counter() - start
        results["new_boundary"] = {
            "success": d_new is not None,
            "d": d_new,
            "time": time_new,
            "boundary": self.new_boundary.get_boundary(n)
        }
        
        return results

