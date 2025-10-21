"""
RSA Weak Key Generator for Wiener Attack Testing

Pure algorithm with no I/O operations.
"""

import random
from typing import Tuple, Dict, Any
from Crypto.Util.number import getPrime, inverse, GCD
from .math_utils import isqrt


class WeakRSAGenerator:
    """Generate weak RSA keys vulnerable to Wiener attack"""
    
    def generate_weak_rsa(self, bits: int = 1024, d_ratio: float = 0.25) -> Tuple[int, int, int, int, int]:
        """
        Generate RSA keypair with small private key
        
        Args:
            bits: Bit length of RSA modulus
            d_ratio: Ratio of d relative to N, controls size of d
                    - Wiener attack: d < N^0.25 / 3
                    - Bunder-Tonien: d < 2*sqrt(2*N)
                    - New boundary: d < sqrt(8.24264*N)
        
        Returns:
            (n, e, d, p, q): RSA parameters
        """
        # Generate two large primes
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)
        
        while p == q:
            q = getPrime(bits // 2)
        
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # Calculate target d size based on ratio
        target_d_bits = int(bits * d_ratio)
        
        # Generate small d
        d = self._generate_small_d(phi, target_d_bits)
        
        # Calculate corresponding e
        try:
            e = inverse(d, phi)
        except:
            # If d and phi are not coprime, regenerate
            return self.generate_weak_rsa(bits, d_ratio)
        
        return n, e, d, p, q
    
    def _generate_small_d(self, phi: int, target_bits: int) -> int:
        """Generate small private key d with specified bit length"""
        max_attempts = 1000
        
        for _ in range(max_attempts):
            # Generate random number with target bit length
            d = random.randrange(2**(target_bits - 1), 2**target_bits)
            
            # Ensure d is coprime with phi
            if GCD(d, phi) == 1:
                return d
        
        # Fallback: use simple method
        d = 3
        while GCD(d, phi) != 1:
            d += 2
        return d
    
    def generate_by_boundary(self, bits: int = 1024, attack_type: str = "wiener") -> Tuple[int, int, int, int, int, int]:
        """
        Generate weak RSA key based on attack type boundary
        
        Args:
            bits: Bit length of RSA modulus
            attack_type: "wiener", "bunder_tonien", or "new_boundary"
        
        Returns:
            (n, e, d, p, q, boundary): RSA parameters and theoretical boundary
        """
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)
        
        while p == q:
            q = getPrime(bits // 2)
        
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # Calculate boundary based on attack type
        if attack_type == "wiener":
            # d < N^0.25 / 3
            boundary = int(pow(n, 0.25) / 3)
        elif attack_type == "bunder_tonien":
            # d < 2*sqrt(2*N)
            boundary = 2 * isqrt(2 * n)
        elif attack_type == "new_boundary":
            # d < sqrt(8.24264*N)
            # 8.24264 ≈ 824264/100000
            boundary = isqrt(824264 * n // 100000)
        else:
            raise ValueError(f"Unknown attack type: {attack_type}")
        
        # Generate d below boundary
        d = self._generate_d_below_boundary(phi, boundary)
        
        # Calculate e
        try:
            e = inverse(d, phi)
        except:
            return self.generate_by_boundary(bits, attack_type)
        
        return n, e, d, p, q, boundary
    
    def _generate_d_below_boundary(self, phi: int, boundary: int) -> int:
        """Generate d below specified boundary"""
        max_attempts = 1000

        # Ensure boundary is integer
        if isinstance(boundary, float):
            boundary = int(boundary)

        # Ensure boundary is not too small
        if boundary < 100:
            boundary = 100

        # Ensure boundary is less than phi
        boundary = min(boundary, phi - 1)

        for _ in range(max_attempts):
            # Random selection within boundary, strongly biased towards smaller values
            # Use very small d to ensure attack success
            upper = max(100000, boundary // 1000)  # Use 0.1% of boundary
            lower = 3

            if lower >= upper:
                upper = max(10000, min(100000, boundary))

            d = random.randrange(lower, upper)

            if GCD(d, phi) == 1:
                return d

        # Fallback: search from small values
        d = 3
        while d < boundary and GCD(d, phi) != 1:
            d += 2

        if d >= boundary:
            d = boundary - 1
            while d > 2 and GCD(d, phi) != 1:
                d -= 2

        return d
    
    def check_vulnerability(self, n: int, d: int) -> Dict[str, Any]:
        """
        Check RSA key vulnerability to various Wiener attacks
        
        Returns:
            dict: Dictionary containing boundary and vulnerability information
        """
        # Import here to avoid circular dependency
        from .wiener import WienerAttack, BunderTonienAttack, NewBoundaryAttack
        
        wiener_attack = WienerAttack()
        bunder_tonien_attack = BunderTonienAttack()
        new_boundary_attack = NewBoundaryAttack()
        
        wiener_bound = wiener_attack.get_boundary(n)
        bt_bound = bunder_tonien_attack.get_boundary(n)
        new_bound = new_boundary_attack.get_boundary(n)
        
        return {
            'd': d,
            'd_bits': d.bit_length(),
            'wiener_bound': wiener_bound,
            'wiener_bound_bits': wiener_bound.bit_length() if wiener_bound > 0 else 0,
            'wiener_vulnerable': d < wiener_bound,
            'bunder_tonien_bound': bt_bound,
            'bunder_tonien_bound_bits': bt_bound.bit_length() if bt_bound > 0 else 0,
            'bunder_tonien_vulnerable': d < bt_bound,
            'new_boundary_bound': new_bound,
            'new_boundary_bound_bits': new_bound.bit_length() if new_bound > 0 else 0,
            'new_boundary_vulnerable': d < new_bound
        }

