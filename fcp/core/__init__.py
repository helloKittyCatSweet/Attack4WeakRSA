"""
Core algorithms for Fermat factorization attack on RSA

Pure algorithm module with no I/O operations.
"""

from .fermat import FermatFactorizer
from .primality import PrimalityTester, miller_rabin, next_prime
from .prime_gen import ClosePrimeGenerator
from .rsa import RSAKeyGenerator, RSAEncryptor

__all__ = [
    'FermatFactorizer',
    'PrimalityTester',
    'miller_rabin',
    'next_prime',
    'ClosePrimeGenerator',
    'RSAKeyGenerator',
    'RSAEncryptor',
]

__version__ = '2.0.0'

