import random
from Crypto.Util.number import GCD


class MathUtils:
    """Mathematical utilities for RSA operations"""

    @staticmethod
    def calculate_phi(p, q, r, s):
        """Calculate Euler's totient function for N = p^r * q^s"""
        return (p ** (r - 1)) * (p - 1) * (q ** (s - 1)) * (q - 1)

    @staticmethod
    def validate_parameters(N, e, d, phi):
        """Validate RSA parameters"""
        validations = {
            "GCD(e, φ(N)) = 1": GCD(e, phi) == 1,
            "e*d ≡ 1 mod φ(N)": (e * d) % phi == 1
        }
        return validations

    @staticmethod
    def estimate_search_space(d_bits, exposure_ratio, exposure_type):
        """Estimate the search space size"""
        unknown_bits = int(d_bits * (1 - exposure_ratio))
        search_space = 2 ** unknown_bits
        return search_space, unknown_bits