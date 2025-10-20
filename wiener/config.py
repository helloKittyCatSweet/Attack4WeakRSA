"""
Configuration for Wiener Attack demonstrations
维纳攻击演示配置
"""

# 默认配置
DEFAULT_CONFIG = {
    'bits': 1024,           # RSA模数比特长度
    'd_ratio': 0.25,        # d相对于N的比例
    'attack_type': 'new_boundary',  # 攻击类型
    'verbose': True         # 详细输出
}

# 基准测试配置
BENCHMARK_CONFIGS = [
    {
        'name': 'Small Key (512-bit)',
        'bits': 512,
        'attack_type': 'wiener',
        'description': '小密钥测试 - Wiener攻击'
    },
    {
        'name': 'Medium Key (1024-bit)',
        'bits': 1024,
        'attack_type': 'bunder_tonien',
        'description': '中等密钥测试 - Bunder-Tonien攻击'
    },
    {
        'name': 'Large Key (2048-bit)',
        'bits': 2048,
        'attack_type': 'new_boundary',
        'description': '大密钥测试 - 新边界攻击'
    },
    {
        'name': 'Very Large Key (4096-bit)',
        'bits': 4096,
        'attack_type': 'new_boundary',
        'description': '超大密钥测试 - 新边界攻击'
    }
]

# 论文中的实验配置（复现论文结果）
PAPER_CONFIGS = [
    {'bits': 1024, 'description': '1024-bit RSA'},
    {'bits': 2048, 'description': '2048-bit RSA'},
    {'bits': 4096, 'description': '4096-bit RSA'},
    {'bits': 8192, 'description': '8192-bit RSA'}
]

# 边界测试配置
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

# 安全参数范围
SAFE_PARAMETERS = {
    'min_bits': 512,
    'max_bits': 8192,
    'recommended_bits': 2048
}

