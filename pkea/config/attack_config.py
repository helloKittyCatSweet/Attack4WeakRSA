#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Centralized configuration for RSA Partial Key Exposure Attack

Defines all parameters for RSA generation, attack execution, and experiments.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class RSAConfig:
    """
    Configuration for RSA parameter generation
    
    Attributes:
        bit_length: Bit length of each prime factor
        r: Exponent of p in modulus (N = p^r * q^s)
        s: Exponent of q in modulus
        e: Public exponent (default: 65537)
    """
    bit_length: int = 20
    r: int = 2
    s: int = 1
    e: int = 65537
    
    def __post_init__(self):
        """Validate configuration"""
        if self.bit_length < 8:
            raise ValueError(f"bit_length must be >= 8, got {self.bit_length}")
        if self.r < 1 or self.s < 1:
            raise ValueError(f"r and s must be >= 1, got r={self.r}, s={self.s}")
        if self.e < 3:
            raise ValueError(f"e must be >= 3, got {self.e}")


@dataclass
class ExperimentConfig:
    """
    Configuration for attack experiments
    
    Attributes:
        delta: Fraction of private key bits known (0 < delta < 1)
        exposure_type: Type of exposure ("MSB" or "LSB")
        m: Lattice dimension parameter
        t: Extra shift parameter
        description: Human-readable description
    """
    delta: float = 0.7
    exposure_type: str = "MSB"
    m: int = 3
    t: int = 2
    description: str = "Default configuration"
    
    def __post_init__(self):
        """Validate configuration"""
        if not (0 < self.delta < 1):
            raise ValueError(f"delta must be in (0, 1), got {self.delta}")
        if self.exposure_type.upper() not in ("MSB", "LSB"):
            raise ValueError(f"exposure_type must be 'MSB' or 'LSB', got {self.exposure_type}")
        if self.m < 1 or self.t < 0:
            raise ValueError(f"m must be >= 1 and t >= 0, got m={self.m}, t={self.t}")
        
        # Normalize exposure_type
        self.exposure_type = self.exposure_type.upper()


# Default configurations
DEFAULT_RSA_CONFIG = RSAConfig(
    bit_length=20,
    r=2,
    s=1,
    e=65537
)

DEFAULT_EXPERIMENT_CONFIG = ExperimentConfig(
    delta=0.7,
    exposure_type="MSB",
    m=3,
    t=2,
    description="Default: 70% MSB exposure"
)


def get_attack_params_for_bit_length(bit_length: int) -> Tuple[int, int]:
    """
    Get recommended attack parameters (m, t) based on problem size
    
    Args:
        bit_length: Bit length of prime factors
        
    Returns:
        Tuple (m, t) with recommended parameters
        
    Recommendations:
        - Small (≤20 bits): m=2, t=1 (fast, sufficient)
        - Medium (21-30 bits): m=3, t=2 (balanced)
        - Large (>30 bits): m=4, t=2 (better success rate)
    """
    if bit_length <= 20:
        return (2, 1)
    elif bit_length <= 30:
        return (3, 2)
    else:
        return (4, 2)


# Predefined experiment configurations
EXPERIMENT_PRESETS = {
    "small_high_exposure": ExperimentConfig(
        delta=0.7,
        exposure_type="MSB",
        m=2,
        t=1,
        description="Small parameters, high exposure (70% MSB)"
    ),
    
    "medium_balanced": ExperimentConfig(
        delta=0.6,
        exposure_type="MSB",
        m=3,
        t=2,
        description="Medium parameters, balanced (60% MSB)"
    ),
    
    "standard_rsa": ExperimentConfig(
        delta=0.7,
        exposure_type="MSB",
        m=3,
        t=2,
        description="Standard RSA (r=1, s=1)"
    ),
    
    "lsb_exposure": ExperimentConfig(
        delta=0.7,
        exposure_type="LSB",
        m=3,
        t=2,
        description="LSB exposure (70%)"
    ),
}


def get_preset(name: str) -> ExperimentConfig:
    """
    Get predefined experiment configuration
    
    Args:
        name: Preset name (see EXPERIMENT_PRESETS keys)
        
    Returns:
        ExperimentConfig for the preset
        
    Raises:
        KeyError: If preset name not found
    """
    if name not in EXPERIMENT_PRESETS:
        available = ", ".join(EXPERIMENT_PRESETS.keys())
        raise KeyError(f"Unknown preset '{name}'. Available: {available}")
    return EXPERIMENT_PRESETS[name]

