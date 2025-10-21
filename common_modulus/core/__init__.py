"""
Common Modulus Attack - Core Module

This module contains the core implementation of the Common Modulus Attack
on RSA and ECC-RSA variants.
"""

from .extended_gcd import extended_gcd, mod_inverse
from .rsa_attack import CommonModulusAttack
from .ecc_rsa_attack import ECCRSACommonModulusAttack

__all__ = [
    'extended_gcd',
    'mod_inverse',
    'CommonModulusAttack',
    'ECCRSACommonModulusAttack',
]

__version__ = '1.0.0'

