"""
Attack orchestration layer for RSA Partial Key Exposure Attack

This module contains attack workflow and verification logic:
- Unified attack interface
- Exposure model (MSB/LSB handling)
- Result verification
"""

from .partial_key_attack import PartialKeyExposureAttack
from .exposure_model import simulate_exposure, ExposureType
from .verifier import verify_private_key, verify_encryption_decryption

__all__ = [
    'PartialKeyExposureAttack',
    'simulate_exposure',
    'ExposureType',
    'verify_private_key',
    'verify_encryption_decryption',
]

