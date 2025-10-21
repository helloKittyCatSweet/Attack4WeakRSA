"""
Configuration parameters for Fermat RSA attack demonstration
"""

from dataclasses import dataclass, field


@dataclass
class DemoConfig:
    """
    Configuration for Fermat factorization demo.
    
    Attributes:
        bits: Bit length for prime generation
        max_gap: Maximum gap between close primes
        rounds: Number of timing rounds
        mode: Demo mode ('fermat' or 'rsa')
        message: Message for RSA demo
        public_exponent: RSA public exponent (e)
    """
    bits: int = 60
    max_gap: int = 1 << 14  # 16384
    rounds: int = 1
    mode: str = 'fermat'
    message: str = "NTU close-primes RSA demo"
    public_exponent: int = 65537

    def __post_init__(self):
        """Validate configuration after initialization"""
        if self.bits < 8:
            raise ValueError(f"bits must be >= 8, got {self.bits}")
        if self.max_gap < 2:
            raise ValueError(f"max_gap must be >= 2, got {self.max_gap}")
        if self.rounds < 1:
            raise ValueError(f"rounds must be >= 1, got {self.rounds}")
        if self.mode not in ('fermat', 'rsa'):
            raise ValueError(f"mode must be 'fermat' or 'rsa', got {self.mode}")


@dataclass
class SafeParameters:
    """
    Safe parameter ranges for demonstration.
    
    Attributes:
        min_bits: Minimum allowed bit length
        max_bits: Maximum recommended bit length
        max_gap_limit: Maximum recommended gap
    """
    min_bits: int = 40
    max_bits: int = 128  # For reasonable demo times
    max_gap_limit: int = 1 << 20  # 1048576

    def is_safe(self, bits: int, max_gap: int) -> bool:
        """
        Check if parameters are within safe ranges.
        
        Args:
            bits: Bit length to check
            max_gap: Gap to check
            
        Returns:
            True if parameters are safe
        """
        return (self.min_bits <= bits <= self.max_bits and 
                max_gap <= self.max_gap_limit)


# Default configuration instance
DEFAULT_CONFIG = DemoConfig()

# Safe parameters instance
SAFE_PARAMETERS = SafeParameters()

