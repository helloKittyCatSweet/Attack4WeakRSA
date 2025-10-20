#!/usr/bin/env python3
"""
Configuration for Common Modulus Attack
同模数攻击配置文件
"""

# 论文中的示例参数
PAPER_EXAMPLE = {
    'name': 'Boudabra & Nitaj ECC-RSA Example',
    'N': 181603559630213323475279432919469869812801,
    'e1': 233,
    'e2': 151,
    'M': {
        'r': 276576193905959805653341,
        'y_M': 24123988022450690140866
    },
    'C1': {
        'r': 165824579408065034165410,
        'y_C1': 127733294106034267552844
    },
    'C2': {
        'r': 165824579408065034165410,
        'y_C2': 53870265524179202259957
    },
    'expected_x': 35,
    'expected_y': -54
}

# 测试配置
TEST_CONFIGS = {
    'small': {
        'name': 'Small RSA (512-bit)',
        'bits': 512,
        'e1': 3,
        'e2': 5,
        'message': 123456789
    },
    'medium': {
        'name': 'Medium RSA (1024-bit)',
        'bits': 1024,
        'e1': 7,
        'e2': 11,
        'message': 987654321
    },
    'large': {
        'name': 'Large RSA (2048-bit)',
        'bits': 2048,
        'e1': 17,
        'e2': 257,
        'message': 1234567890123456789
    }
}

# 椭圆曲线参数（用于ECC-RSA变体）
ECC_PARAMS = {
    'a': 1,
    'b': 1,
    'p': 181603559630213323475279432919469869812801  # 与N相同
}

# 输出配置
OUTPUT_CONFIG = {
    'verbose': True,
    'show_steps': True,
    'show_verification': True
}

