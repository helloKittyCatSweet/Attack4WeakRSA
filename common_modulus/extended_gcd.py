#!/usr/bin/env python3
"""
Extended Euclidean Algorithm
扩展欧几里得算法

用于求解 ax + by = gcd(a, b) 中的 x 和 y
"""


def extended_gcd(a, b):
    """
    扩展欧几里得算法
    
    求解: ax + by = gcd(a, b)
    
    Args:
        a: 第一个整数
        b: 第二个整数
    
    Returns:
        (gcd, x, y): 最大公约数和贝祖系数
        满足 a*x + b*y = gcd(a, b)
    
    Example:
        >>> extended_gcd(233, 151)
        (1, 35, -54)
        验证: 233*35 + 151*(-54) = 8155 - 8154 = 1 ✓
    """
    if b == 0:
        return a, 1, 0
    
    # 保存原始值用于验证
    orig_a, orig_b = a, b
    
    # 初始化
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    # 迭代计算
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    
    gcd = old_r
    x = old_s
    y = old_t
    
    # 验证结果
    assert orig_a * x + orig_b * y == gcd, f"验证失败: {orig_a}*{x} + {orig_b}*{y} != {gcd}"
    
    return gcd, x, y


def extended_gcd_verbose(a, b):
    """
    扩展欧几里得算法（详细版本，显示计算步骤）
    
    Args:
        a: 第一个整数
        b: 第二个整数
    
    Returns:
        (gcd, x, y): 最大公约数和贝祖系数
    """
    print(f"\n{'='*70}")
    print(f"扩展欧几里得算法: 求解 {a}x + {b}y = gcd({a}, {b})")
    print(f"{'='*70}")
    
    if b == 0:
        print(f"\n基础情况: b = 0")
        print(f"结果: gcd = {a}, x = 1, y = 0")
        return a, 1, 0
    
    orig_a, orig_b = a, b
    
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    print(f"\n初始化:")
    print(f"  r₀ = {old_r}, r₁ = {r}")
    print(f"  s₀ = {old_s}, s₁ = {s}")
    print(f"  t₀ = {old_t}, t₁ = {t}")
    
    print(f"\n迭代过程:")
    print(f"{'步骤':<6} {'商q':<10} {'r':<20} {'s':<15} {'t':<15}")
    print("-" * 70)
    
    step = 0
    while r != 0:
        quotient = old_r // r
        
        new_r = old_r - quotient * r
        new_s = old_s - quotient * s
        new_t = old_t - quotient * t
        
        print(f"{step:<6} {quotient:<10} {r:<20} {s:<15} {t:<15}")
        
        old_r, r = r, new_r
        old_s, s = s, new_s
        old_t, t = t, new_t
        
        step += 1
    
    gcd = old_r
    x = old_s
    y = old_t
    
    print(f"\n最终结果:")
    print(f"  gcd({orig_a}, {orig_b}) = {gcd}")
    print(f"  x = {x}")
    print(f"  y = {y}")
    
    # 验证
    result = orig_a * x + orig_b * y
    print(f"\n验证:")
    print(f"  {orig_a} × {x} + {orig_b} × {y} = {result}")
    print(f"  {'✓ 正确' if result == gcd else '✗ 错误'}")
    
    return gcd, x, y


def mod_inverse(a, m):
    """
    计算模逆元
    
    求解 a * x ≡ 1 (mod m) 中的 x
    
    Args:
        a: 整数
        m: 模数
    
    Returns:
        x: 模逆元，如果不存在则返回 None
    
    Example:
        >>> mod_inverse(3, 11)
        4
        验证: 3 * 4 = 12 ≡ 1 (mod 11) ✓
    """
    gcd, x, _ = extended_gcd(a, m)
    
    if gcd != 1:
        return None  # 模逆元不存在
    
    return x % m


def test_extended_gcd():
    """测试扩展欧几里得算法"""
    print("\n" + "="*70)
    print("扩展欧几里得算法测试")
    print("="*70)
    
    test_cases = [
        (233, 151),  # 论文示例
        (240, 46),
        (17, 13),
        (1071, 462),
        (65537, 3)
    ]
    
    for a, b in test_cases:
        gcd, x, y = extended_gcd(a, b)
        result = a * x + b * y
        
        print(f"\ngcd({a}, {b}) = {gcd}")
        print(f"  {a} × {x} + {b} × {y} = {result}")
        print(f"  验证: {'✓' if result == gcd else '✗'}")


if __name__ == "__main__":
    # 测试基本功能
    test_extended_gcd()
    
    # 详细演示论文示例
    print("\n\n" + "="*70)
    print("论文示例详细演示")
    print("="*70)
    extended_gcd_verbose(233, 151)

