#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified interface for partial key exposure attack

Orchestrates the complete attack workflow.
"""

from typing import Optional, Tuple
from dataclasses import dataclass
import time


@dataclass
class AttackConfig:
    """
    Configuration for attack
    
    Attributes:
        m: Lattice dimension parameter
        t: Extra shift parameter
        max_search: Maximum search range for roots
    """
    m: int = 3
    t: int = 2
    max_search: int = 10000


@dataclass
class AttackResult:
    """
    Result of attack
    
    Attributes:
        success: Whether attack succeeded
        x_recovered: Recovered unknown part (None if failed)
        d_recovered: Recovered private key (None if failed)
        elapsed_time: Time taken in seconds
        details: Additional details
    """
    success: bool
    x_recovered: Optional[int]
    d_recovered: Optional[int]
    elapsed_time: float
    details: str = ""


class PartialKeyExposureAttack:
    """
    Unified interface for partial key exposure attack
    
    Encapsulates the complete attack workflow:
    1. Setup with RSA parameters and partial key knowledge
    2. Execute Coppersmith attack
    3. Recover full private key
    4. Verify results
    
    Example:
        >>> from attack import PartialKeyExposureAttack
        >>> from attack.exposure_model import simulate_exposure
        >>> 
        >>> # Setup
        >>> N, e, d, p, q, phi = generate_small_rsa_params(20, 2, 1)
        >>> exposure = simulate_exposure(d, 0.7, "MSB")
        >>> 
        >>> # Attack
        >>> attack = PartialKeyExposureAttack(N, e, phi, exposure.d0, exposure.X)
        >>> result = attack.run()
        >>> 
        >>> if result.success:
        >>>     print(f"Recovered d = {result.d_recovered}")
    """

    def __init__(self, N: int, e: int, M: int, d0: int, X: int, config: Optional[AttackConfig] = None):
        """
        Initialize attack
        
        Args:
            N: RSA modulus
            e: Public exponent
            M: Modulus for polynomial (typically φ(N))
            d0: Known part of private key
            X: Upper bound on unknown part
            config: Attack configuration (optional)
        """
        self.N = N
        self.e = e
        self.M = M
        self.d0 = d0
        self.X = X
        self.config = config or AttackConfig()

    def run(self) -> AttackResult:
        """
        Execute the attack

        Returns:
            AttackResult with success status and recovered values
        """
        # Import here to avoid circular dependency
        try:
            from core.coppersmith_attack import improved_coppersmith_attack
        except ImportError:
            from ..core.coppersmith_attack import improved_coppersmith_attack
        
        start_time = time.time()
        
        try:
            # Execute Coppersmith attack
            x_recovered = improved_coppersmith_attack(
                self.N, self.e, self.d0, self.X, self.M,
                m=self.config.m, t=self.config.t
            )
            
            elapsed_time = time.time() - start_time
            
            if x_recovered is not None:
                # Success - we don't know exposure type here, so just return x
                # The caller will reconstruct d based on their exposure model
                return AttackResult(
                    success=True,
                    x_recovered=x_recovered,
                    d_recovered=None,  # Caller will reconstruct
                    elapsed_time=elapsed_time,
                    details=f"Recovered x = {x_recovered}"
                )
            else:
                return AttackResult(
                    success=False,
                    x_recovered=None,
                    d_recovered=None,
                    elapsed_time=elapsed_time,
                    details="No valid root found"
                )
                
        except Exception as e:
            elapsed_time = time.time() - start_time
            return AttackResult(
                success=False,
                x_recovered=None,
                d_recovered=None,
                elapsed_time=elapsed_time,
                details=f"Error: {str(e)}"
            )

    def run_with_verification(self, d_true: int, exposure_type, known_bits: int) -> Tuple[AttackResult, Optional['VerificationResult']]:
        """
        Execute attack and verify results

        Args:
            d_true: True private key (for verification)
            exposure_type: Type of exposure (MSB/LSB)
            known_bits: Number of known bits

        Returns:
            Tuple of (AttackResult, VerificationResult)
        """
        try:
            from attack.exposure_model import recover_private_key
            from attack.verifier import full_verification
        except ImportError:
            from .exposure_model import recover_private_key
            from .verifier import full_verification
        
        # Run attack
        attack_result = self.run()
        
        if not attack_result.success:
            return attack_result, None
        
        # Recover full private key
        d_recovered = recover_private_key(
            self.d0, attack_result.x_recovered, exposure_type, known_bits
        )
        attack_result.d_recovered = d_recovered
        
        # Verify
        verification = full_verification(d_true, d_recovered, self.e, self.N, self.M)
        
        return attack_result, verification

