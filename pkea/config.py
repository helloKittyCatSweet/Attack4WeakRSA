# Configuration parameters
CONFIG = {
    'n_bits': 64,  # Using 64-bit for demonstration
    'r': 2,
    's': 1,
    'exposure_ratio': 0.7,  # 70% key exposure
    'exposure_type': 'MSB',  # MSB exposure
    'num_threads': 4,
    'timeout': 30  # 30-second timeout
}

BENCHMARK_CONFIGS = [
    {'n_bits': 48, 'ratio': 0.6, 'threads': 2, 'desc': 'Small scale test'},
    {'n_bits': 64, 'ratio': 0.7, 'threads': 4, 'desc': 'Medium scale'},
    {'n_bits': 80, 'ratio': 0.8, 'threads': 8, 'desc': 'Large scale'},
]