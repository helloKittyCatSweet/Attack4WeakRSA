"""
Configuration module for RSA Partial Key Exposure Attack

Centralized configuration management.
"""

from .attack_config import (
    RSAConfig,
    ExperimentConfig,
    DEFAULT_RSA_CONFIG,
    DEFAULT_EXPERIMENT_CONFIG,
    get_attack_params_for_bit_length
)

__all__ = [
    'RSAConfig',
    'ExperimentConfig',
    'DEFAULT_RSA_CONFIG',
    'DEFAULT_EXPERIMENT_CONFIG',
    'get_attack_params_for_bit_length',
]

