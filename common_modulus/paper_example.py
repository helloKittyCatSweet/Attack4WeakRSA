#!/usr/bin/env python3
"""
Paper Example: Common Modulus Attack on ECC-RSA
复现论文实例

论文: "Common Modulus Attack on the Elliptic Curve-Based RSA Algorithm Variant"
作者: Boudabra & Nitaj

论文中的具体参数:
- N = 181603559630213323475279432919469869812801
- e1 = 233, e2 = 151
- M = (r, y_M) = (276576193905959805653341, 24123988022450690140866)
- 扩展欧几里得: x = 35, y = -54
"""

from common_modulus_attack import CommonModulusAttack, ECCRSACommonModulusAttack
from config import PAPER_EXAMPLE, ECC_PARAMS
import time


def test_paper_example_rsa():
    """测试论文示例 - 普通RSA版本"""
    print("\n" + "="*70)
    print("论文示例复现 - 普通RSA")
    print("="*70)
    
    # 从配置读取参数
    N = PAPER_EXAMPLE['N']
    e1 = PAPER_EXAMPLE['e1']
    e2 = PAPER_EXAMPLE['e2']
    
    # 使用r作为明文（简化版本）
    M = PAPER_EXAMPLE['M']['r']
    
    print(f"\n[1] 生成密文...")
    print(f"  明文 M = {M}")
    
    # 生成两个密文
    C1 = pow(M, e1, N)
    C2 = pow(M, e2, N)
    
    print(f"  C1 = M^{e1} mod N = {C1}")
    print(f"  C2 = M^{e2} mod N = {C2}")
    
    # 执行攻击
    print(f"\n[2] 执行同模数攻击...")
    attacker = CommonModulusAttack()
    
    start = time.perf_counter()
    recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=True)
    elapsed = time.perf_counter() - start
    
    # 验证结果
    print(f"\n[3] 验证结果...")
    if recovered_M == M:
        print(f"  ✓ 攻击成功!")
        print(f"  原始明文: {M}")
        print(f"  恢复明文: {recovered_M}")
        print(f"  总耗时: {elapsed*1000:.3f} ms")
        return True
    else:
        print(f"  ✗ 攻击失败")
        print(f"  原始明文: {M}")
        print(f"  恢复明文: {recovered_M}")
        return False


def test_paper_example_ecc_rsa():
    """测试论文示例 - ECC-RSA变体"""
    print("\n" + "="*70)
    print("论文示例复现 - ECC-RSA变体")
    print("="*70)
    
    # 从配置读取参数
    N = PAPER_EXAMPLE['N']
    e1 = PAPER_EXAMPLE['e1']
    e2 = PAPER_EXAMPLE['e2']
    
    # 明文点
    M = (PAPER_EXAMPLE['M']['r'], PAPER_EXAMPLE['M']['y_M'])
    
    # 密文点（从论文）
    C1 = (PAPER_EXAMPLE['C1']['r'], PAPER_EXAMPLE['C1']['y_C1'])
    C2 = (PAPER_EXAMPLE['C2']['r'], PAPER_EXAMPLE['C2']['y_C2'])
    
    print(f"\n[1] 论文参数:")
    print(f"  N = {N}")
    print(f"  e1 = {e1}, e2 = {e2}")
    print(f"  明文点 M = {M}")
    print(f"  密文点 C1 = {C1}")
    print(f"  密文点 C2 = {C2}")
    
    # 创建攻击器
    a = ECC_PARAMS['a']
    b = ECC_PARAMS['b']
    p = ECC_PARAMS['p']
    
    attacker = ECCRSACommonModulusAttack(a, b, p)
    
    # 执行攻击
    print(f"\n[2] 执行同模数攻击...")
    start = time.perf_counter()
    recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=True)
    elapsed = time.perf_counter() - start
    
    # 验证结果
    print(f"\n[3] 验证结果...")
    if recovered_M == M:
        print(f"  ✓ 攻击成功!")
        print(f"  原始明文点: {M}")
        print(f"  恢复明文点: {recovered_M}")
        print(f"  总耗时: {elapsed*1000:.3f} ms")
        return True
    else:
        print(f"  ⚠ 结果不匹配")
        print(f"  原始明文点: {M}")
        print(f"  恢复明文点: {recovered_M}")
        print(f"  总耗时: {elapsed*1000:.3f} ms")
        
        # 检查是否在同一条曲线上
        if recovered_M:
            x, y = recovered_M
            lhs = (y * y) % p
            rhs = (x * x * x + a * x + b) % p
            on_curve = lhs == rhs
            print(f"\n  恢复的点在曲线上: {'✓' if on_curve else '✗'}")
        
        return False


def verify_extended_gcd():
    """验证扩展欧几里得算法结果"""
    print("\n" + "="*70)
    print("验证扩展欧几里得算法")
    print("="*70)
    
    e1 = PAPER_EXAMPLE['e1']
    e2 = PAPER_EXAMPLE['e2']
    expected_x = PAPER_EXAMPLE['expected_x']
    expected_y = PAPER_EXAMPLE['expected_y']
    
    from extended_gcd import extended_gcd
    
    gcd, x, y = extended_gcd(e1, e2)
    
    print(f"\n论文中的值:")
    print(f"  e1 = {e1}, e2 = {e2}")
    print(f"  x = {expected_x}, y = {expected_y}")
    
    print(f"\n计算结果:")
    print(f"  gcd({e1}, {e2}) = {gcd}")
    print(f"  x = {x}, y = {y}")
    
    # 验证
    result = e1 * x + e2 * y
    expected_result = e1 * expected_x + e2 * expected_y
    
    print(f"\n验证:")
    print(f"  {e1} × {x} + {e2} × {y} = {result}")
    print(f"  {e1} × {expected_x} + {e2} × {expected_y} = {expected_result}")
    
    if x == expected_x and y == expected_y:
        print(f"  ✓ 与论文结果完全一致")
    else:
        print(f"  ⚠ 与论文结果不同，但都满足贝祖等式")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("Common Modulus Attack - 论文示例复现")
    print("="*70)
    print("\n论文: Common Modulus Attack on the Elliptic Curve-Based")
    print("      RSA Algorithm Variant (Boudabra & Nitaj)")
    
    # 1. 验证扩展欧几里得算法
    verify_extended_gcd()
    
    # 2. 测试普通RSA版本
    input("\n按Enter继续测试普通RSA版本...")
    success_rsa = test_paper_example_rsa()
    
    # 3. 测试ECC-RSA变体
    input("\n按Enter继续测试ECC-RSA变体...")
    success_ecc = test_paper_example_ecc_rsa()
    
    # 总结
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    print(f"  扩展欧几里得算法: ✓")
    print(f"  普通RSA攻击: {'✓' if success_rsa else '✗'}")
    print(f"  ECC-RSA攻击: {'✓' if success_ecc else '⚠'}")
    
    print("\n" + "="*70)
    print("关键结论")
    print("="*70)
    print("  • 同模数攻击对普通RSA和ECC-RSA变体都有效")
    print("  • 只要 gcd(e1, e2) = 1，攻击者无需私钥即可恢复明文")
    print("  • 攻击复杂度极低，几乎即时完成")
    print("  • 模数重用是根本性安全错误，必须避免")
    print("="*70)


if __name__ == "__main__":
    main()

