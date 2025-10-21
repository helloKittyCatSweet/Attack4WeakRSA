"""
Parameter validation utilities (no print, returns results)
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ValidationResult:
    """
    Result of parameter validation.
    
    Attributes:
        valid: Whether parameters are valid
        warnings: List of warning messages
        errors: List of error messages
    """
    valid: bool
    warnings: List[str]
    errors: List[str]

    def has_warnings(self) -> bool:
        """Check if there are any warnings"""
        return len(self.warnings) > 0

    def has_errors(self) -> bool:
        """Check if there are any errors"""
        return len(self.errors) > 0


def validate_parameters(bits: int, max_gap: int, safe_params: Dict[str, Any]) -> ValidationResult:
    """
    Validate that parameters are within safe demonstration ranges.

    Args:
        bits: Bit length for primes
        max_gap: Maximum gap between primes
        safe_params: Dictionary with keys:
            - 'min_bits': Minimum allowed bits
            - 'max_bits': Maximum recommended bits
            - 'max_gap_limit': Maximum recommended gap

    Returns:
        ValidationResult with validation status and messages

    Example:
        >>> safe = {'min_bits': 40, 'max_bits': 128, 'max_gap_limit': 1<<20}
        >>> result = validate_parameters(60, 1<<14, safe)
        >>> result.valid
        True
        >>> result.has_warnings()
        False
    """
    warnings = []
    errors = []

    # Check minimum bits
    if bits < safe_params['min_bits']:
        errors.append(f"bits={bits} too small, minimum is {safe_params['min_bits']}")

    # Check maximum bits (warning only)
    if bits > safe_params['max_bits']:
        warnings.append(f"bits={bits} is large, may take long time (recommended max: {safe_params['max_bits']})")

    # Check max_gap (warning only)
    if max_gap > safe_params['max_gap_limit']:
        warnings.append(f"max_gap={max_gap} is large, may take long time (recommended max: {safe_params['max_gap_limit']})")

    # Check for negative values
    if bits < 0:
        errors.append(f"bits={bits} cannot be negative")
    
    if max_gap < 0:
        errors.append(f"max_gap={max_gap} cannot be negative")

    valid = len(errors) == 0

    return ValidationResult(valid=valid, warnings=warnings, errors=errors)


def validate_rsa_parameters(e: int, n: int) -> ValidationResult:
    """
    Validate RSA public key parameters.

    Args:
        e: Public exponent
        n: Modulus

    Returns:
        ValidationResult with validation status

    Example:
        >>> result = validate_rsa_parameters(65537, 3233)
        >>> result.valid
        True
    """
    warnings = []
    errors = []

    # Check e is odd and > 1
    if e <= 1:
        errors.append(f"Public exponent e={e} must be > 1")
    elif e % 2 == 0:
        errors.append(f"Public exponent e={e} must be odd")

    # Check n is odd and > 1
    if n <= 1:
        errors.append(f"Modulus n={n} must be > 1")
    elif n % 2 == 0:
        warnings.append(f"Modulus n={n} is even (unusual for RSA)")

    # Check e < n
    if e >= n:
        errors.append(f"Public exponent e={e} must be < n={n}")

    valid = len(errors) == 0

    return ValidationResult(valid=valid, warnings=warnings, errors=errors)

