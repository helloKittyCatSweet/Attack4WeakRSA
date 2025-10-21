#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exposure model for partial key exposure attack

Handles MSB/LSB exposure scenarios.
"""

from enum import Enum
from typing import Tuple
from dataclasses import dataclass


class ExposureType(Enum):
    """Type of key exposure"""
    MSB = "MSB"  # Most Significant Bits known
    LSB = "LSB"  # Least Significant Bits known


@dataclass
class ExposureResult:
    """
    Result of exposure simulation
    
    Attributes:
        d0: Known part of private key
        x_true: True unknown part
        X: Upper bound on unknown part
        exposure_type: Type of exposure (MSB/LSB)
        known_bits: Number of known bits
        unknown_bits: Number of unknown bits
    """
    d0: int
    x_true: int
    X: int
    exposure_type: ExposureType
    known_bits: int
    unknown_bits: int
    
    def verify_reconstruction(self, d: int) -> bool:
        """
        Verify that d0 and x_true correctly reconstruct d
        
        Args:
            d: Original private key
            
        Returns:
            True if reconstruction is correct
        """
        if self.exposure_type == ExposureType.MSB:
            return d == self.d0 + self.x_true
        else:  # LSB
            return d == (self.x_true << self.known_bits) + self.d0


def simulate_exposure(d: int, delta: float, exposure_type: str) -> ExposureResult:
    """
    Simulate partial key exposure
    
    Given a private key d and exposure ratio delta, simulates either MSB or LSB exposure.
    
    Args:
        d: Private key
        delta: Fraction of bits known (0 < delta < 1)
        exposure_type: "MSB" or "LSB"
        
    Returns:
        ExposureResult containing d0, x_true, X, and metadata
        
    Example:
        >>> d = 12345
        >>> result = simulate_exposure(d, 0.7, "MSB")
        >>> print(f"Known: {result.d0}, Unknown: {result.x_true}, Bound: {result.X}")
    """
    d_bits = d.bit_length()
    known_bits = int(d_bits * delta)
    unknown_bits = d_bits - known_bits
    
    exp_type = ExposureType(exposure_type.upper())

    if exp_type == ExposureType.MSB:
        # MSB known: d = d0 + x where d0 has high bits, x has low bits
        shift = d_bits - known_bits
        d0 = (d >> shift) << shift  # Clear low bits
        x_true = d - d0  # Low bits
        X = 2 ** shift  # Upper bound on x
    else:  # LSB
        # LSB known: d = (x << known_bits) + d0 where d0 has low bits, x has high bits
        mask = (1 << known_bits) - 1
        d0 = d & mask  # Low bits
        x_true = (d - d0) >> known_bits  # High bits
        X = 2 ** unknown_bits  # Upper bound on x

    return ExposureResult(
        d0=d0,
        x_true=x_true,
        X=X,
        exposure_type=exp_type,
        known_bits=known_bits,
        unknown_bits=unknown_bits
    )


def recover_private_key(d0: int, x_recovered: int, exposure_type: ExposureType, known_bits: int) -> int:
    """
    Recover full private key from known part and recovered unknown part
    
    Args:
        d0: Known part of private key
        x_recovered: Recovered unknown part
        exposure_type: Type of exposure
        known_bits: Number of known bits
        
    Returns:
        Recovered private key
    """
    if exposure_type == ExposureType.MSB:
        return d0 + x_recovered
    else:  # LSB
        return (x_recovered << known_bits) + d0

