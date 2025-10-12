"""
Configuration parameters for Fermat RSA attack demonstration
"""

DEFAULT_CONFIG = {
    'bits': 60,
    'max_gap': 1 << 14,
    'rounds': 1,
    'mode': 'fermat',
    'message': "NTU close-primes RSA demo",  # 添加缺失的键
    'public_exponent': 65537
}

# Safe parameter ranges for demonstration
SAFE_PARAMETERS = {
    'min_bits': 40,
    'max_bits': 128,  # For reasonable demo times
    'max_gap_limit': 1 << 20
}