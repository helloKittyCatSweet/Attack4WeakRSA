"""
RSA Partial Key Exposure Attack

A comprehensive implementation of Coppersmith's attack on RSA with partial key exposure.

Modules:
    core: Pure algorithms (polynomial, LLL, Coppersmith, RSA generation)
    attack: Attack orchestration (exposure model, verification)
    config: Centralized configuration
    utils: Logging and utilities
    demo: Demonstrations and benchmarks
"""

__version__ = '2.0.0'
__author__ = 'NTU SC6104 Project'

# Expose main interfaces
from .core import (
    Polynomial,
    ImprovedLLL,
    ImprovedMathUtils,
    improved_coppersmith_attack,
    generate_small_rsa_params,
    generate_standard_rsa,
)

from .attack import (
    PartialKeyExposureAttack,
    simulate_exposure,
    ExposureType,
    verify_private_key,
    verify_encryption_decryption,
)

from .config import (
    RSAConfig,
    ExperimentConfig,
    DEFAULT_RSA_CONFIG,
    DEFAULT_EXPERIMENT_CONFIG,
)

from .demo import (
    run_single_attack,
    run_demonstration,
    run_benchmark,
)

__all__ = [
    # Core
    'Polynomial',
    'ImprovedLLL',
    'ImprovedMathUtils',
    'improved_coppersmith_attack',
    'generate_small_rsa_params',
    'generate_standard_rsa',
    
    # Attack
    'PartialKeyExposureAttack',
    'simulate_exposure',
    'ExposureType',
    'verify_private_key',
    'verify_encryption_decryption',
    
    # Config
    'RSAConfig',
    'ExperimentConfig',
    'DEFAULT_RSA_CONFIG',
    'DEFAULT_EXPERIMENT_CONFIG',
    
    # Demo
    'run_single_attack',
    'run_demonstration',
    'run_benchmark',
]

