DEFAULT_CONFIG = {
    'bits': 1024,           # the length of RSA modulus
    'd_ratio': 0.25,
    'attack_type': 'new_boundary',
    'verbose': True
}

BENCHMARK_CONFIGS = [
    {
        'name': 'Small Key (512-bit)',
        'bits': 512,
        'attack_type': 'wiener',
        'description': 'small key - Wiener Attack'
    },
    {
        'name': 'Medium Key (1024-bit)',
        'bits': 1024,
        'attack_type': 'bunder_tonien',
        'description': 'medium key - Bunder-Tonien Attack'
    },
    {
        'name': 'Large Key (2048-bit)',
        'bits': 2048,
        'attack_type': 'new_boundary',
        'description': 'large key - new boundary attack'
    },
    {
        'name': 'Very Large Key (4096-bit)',
        'bits': 4096,
        'attack_type': 'new_boundary',
        'description': 'huge key - new boundary attack'
    }
]

PAPER_CONFIGS = [
    {'bits': 1024, 'description': '1024-bit RSA'},
    {'bits': 2048, 'description': '2048-bit RSA'},
    {'bits': 4096, 'description': '4096-bit RSA'},
    {'bits': 8192, 'description': '8192-bit RSA'}
]

BOUNDARY_TEST_CONFIGS = [
    {
        'name': 'Wiener Boundary Test',
        'bits': 1024,
        'd_ratios': [0.20, 0.22, 0.24, 0.25, 0.26],
        'attack_type': 'wiener'
    },
    {
        'name': 'Bunder-Tonien Boundary Test',
        'bits': 1024,
        'd_ratios': [0.45, 0.48, 0.50, 0.52, 0.55],
        'attack_type': 'bunder_tonien'
    },
    {
        'name': 'New Boundary Test',
        'bits': 1024,
        'd_ratios': [0.48, 0.50, 0.52, 0.54, 0.56],
        'attack_type': 'new_boundary'
    }
]

SAFE_PARAMETERS = {
    'min_bits': 512,
    'max_bits': 8192,
    'recommended_bits': 2048
}

