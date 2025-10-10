#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Partial Key Exposure Attack on RSA with Moduli N = p^r * q^s
基于 Coppersmith 方法和格约简的部分私钥泄露攻击

论文: Partial Key Exposure Attacks on RSA with Moduli N=p^r q^s
实现: 快速演示版本（使用小参数确保几秒内完成）
"""

import time
from sage.all import *
from Crypto.Util.number import getPrime, inverse, GCD
import random

# ============================================================================
# 工具函数
# ============================================================================

def generate_rsa_generalized(bit_length, r, s):
    """
    生成广义 RSA 参数 N = p^r * q^s
    
    参数:
        bit_length: 素数位长
        r, s: 幂次
    返回:
        (N, e, d, p, q, phi)
    """
    print(f"\n[*] 生成广义 RSA 参数 (bit_length={bit_length}, r={r}, s={s})")
    
    # 生成素数
    p = getPrime(bit_length)
    q = getPrime(bit_length)
    while p == q:
        q = getPrime(bit_length)
    
    # 计算 N 和 φ(N)
    N = (p ** r) * (q ** s)
    phi = (p ** (r-1)) * (p - 1) * (q ** (s-1)) * (q - 1)
    
    # 选择公钥 e
    e = 65537
    while GCD(e, phi) != 1:
        e = random.randint(2, phi - 1)
    
    # 计算私钥 d
    d = inverse(e, phi)
    
    print(f"    p = {p}")
    print(f"    q = {q}")
    print(f"    N = {N}")
    print(f"    N 位长 = {N.bit_length()} bits")
    print(f"    e = {e}")
    print(f"    d = {d}")
    print(f"    φ(N) = {phi}")
    
    return N, e, d, p, q, phi


def create_partial_key_exposure(d, delta, exposure_type="MSB"):
    """
    创建部分私钥泄露场景
    
    参数:
        d: 完整私钥
        delta: 泄露比例 (0 < delta < 1)
        exposure_type: "MSB" (最高有效位) 或 "LSB" (最低有效位)
    返回:
        (d0, x, X) - 已知部分、未知部分、未知部分上界
    """
    d_bits = d.bit_length()
    known_bits = int(d_bits * delta)
    
    print(f"\n[*] 创建部分私钥泄露 (δ={delta}, type={exposure_type})")
    print(f"    d 总位长 = {d_bits} bits")
    print(f"    已知位数 = {known_bits} bits")
    print(f"    未知位数 = {d_bits - known_bits} bits")
    
    if exposure_type == "MSB":
        # 已知最高有效位
        shift = d_bits - known_bits
        d0 = (d >> shift) << shift  # 清除低位
        x = d - d0
        X = 2 ** shift
    else:  # LSB
        # 已知最低有效位
        mask = (1 << known_bits) - 1
        d0 = d & mask
        x = d - d0
        X = 2 ** (d_bits - known_bits + 1)
    
    print(f"    d0 (已知) = {d0}")
    print(f"    x (未知) = {x}")
    print(f"    X (上界) = {X}")
    print(f"    验证: d0 + x = {d0 + x} {'✓' if d0 + x == d else '✗'}")
    
    return d0, x, X


# ============================================================================
# Coppersmith 攻击核心
# ============================================================================

def coppersmith_attack_univariate(N, e, d0, X, M, m=2, t=1):
    """
    使用 Coppersmith 方法恢复未知部分 x
    基于单变量多项式的格约简
    
    参数:
        N: RSA 模数
        e: 公钥指数
        d0: 已知的私钥部分
        X: 未知部分 x 的上界
        M: 模数 (通常是 φ(N) 的某个因子)
        m: 格构造参数 (控制格维度)
        t: 额外多项式参数
    返回:
        恢复的 x 值，失败返回 None
    """
    print(f"\n[*] 开始 Coppersmith 格攻击")
    print(f"    格参数: m={m}, t={t}")
    
    # 构造基本多项式 f(x) = e*x + (e*d0 - 1)
    PR.<x> = PolynomialRing(ZZ)
    f = e * x + (e * d0 - 1)
    
    print(f"    基本多项式: f(x) = {f}")
    print(f"    模 M = {M}")
    
    # 构造格基矩阵
    # 使用 x^i * f(x)^j * M^(m-j) 形式的多项式
    polynomials = []
    
    # 第一组: x^i * f(x)^j * M^(m-j), j=0..m-1, i=0..m-j-1
    for j in range(m):
        for i in range(m - j):
            poly = x^i * f^j * M^(m - j)
            polynomials.append(poly)
    
    # 第二组: x^i * f(x)^m, i=0..t-1
    for i in range(t):
        poly = x^i * f^m
        polynomials.append(poly)
    
    # 构造格基矩阵
    n = len(polynomials)
    max_degree = max([poly.degree() for poly in polynomials])
    
    print(f"    格维度: {n} x {n}")
    print(f"    最大次数: {max_degree}")
    
    # 创建矩阵
    L = Matrix(ZZ, n, n)
    
    for i, poly in enumerate(polynomials):
        # 对多项式系数进行缩放: 用 X 替换 x
        for j in range(poly.degree() + 1):
            L[i, j] = poly[j] * (X ^ j)
    
    # LLL 格约简
    print(f"    开始 LLL 格约简...")
    start_time = time.time()
    L_reduced = L.LLL()
    lll_time = time.time() - start_time
    print(f"    LLL 完成，耗时 {lll_time:.3f} 秒")
    
    # 从最短向量重构多项式
    print(f"    从短向量重构多项式...")
    
    for i in range(min(n, 5)):  # 尝试前几个短向量
        # 重构多项式 (除以 X^j)
        coeffs = []
        for j in range(max_degree + 1):
            coeffs.append(L_reduced[i, j] // (X ^ j))
        
        G = PR(coeffs)
        
        # 求根
        roots = G.roots(ring=ZZ)
        
        for root, _ in roots:
            if 0 < root < X:
                print(f"    ✓ 找到候选根: x = {root}")
                # 验证
                if (e * (d0 + root) - 1) % M == 0:
                    print(f"    ✓ 验证成功!")
                    return root
    
    print(f"    ✗ 未找到有效根")
    return None


# ============================================================================
# 主攻击流程
# ============================================================================

def attack_partial_key_exposure(bit_length=64, r=2, s=1, delta=0.5, 
                                 exposure_type="MSB", m=2, t=1):
    """
    完整的部分私钥泄露攻击流程
    
    参数:
        bit_length: 素数位长 (建议 32-128 以确保快速)
        r, s: N = p^r * q^s 的幂次
        delta: 私钥泄露比例
        exposure_type: 泄露类型 ("MSB" 或 "LSB")
        m, t: 格构造参数
    """
    print("=" * 80)
    print("部分私钥泄露攻击 - RSA with N = p^r * q^s")
    print("=" * 80)
    
    total_start = time.time()
    
    # 步骤 1: 生成 RSA 参数
    N, e, d, p, q, phi = generate_rsa_generalized(bit_length, r, s)
    
    # 步骤 2: 创建部分泄露
    d0, x_true, X = create_partial_key_exposure(d, delta, exposure_type)
    
    # 步骤 3: 选择模 M
    # 对于 Scheme 1: M = φ(N)
    # 对于 Scheme 2: M = (p-1)(q-1) 或其他变体
    # 这里使用 φ(N) 作为模
    M = phi
    
    print(f"\n[*] 攻击配置")
    print(f"    模 M = φ(N)")
    print(f"    格参数: m={m}, t={t}")
    
    # 步骤 4: 执行 Coppersmith 攻击
    attack_start = time.time()
    x_recovered = coppersmith_attack_univariate(N, e, d0, X, M, m, t)
    attack_time = time.time() - attack_start
    
    # 步骤 5: 验证结果
    print("\n" + "=" * 80)
    print("攻击结果")
    print("=" * 80)
    
    if x_recovered is not None:
        d_recovered = d0 + x_recovered
        
        print(f"✓ 攻击成功!")
        print(f"  真实 x    = {x_true}")
        print(f"  恢复 x    = {x_recovered}")
        print(f"  匹配      = {x_true == x_recovered}")
        print(f"  真实 d    = {d}")
        print(f"  恢复 d    = {d_recovered}")
        print(f"  匹配      = {d == d_recovered}")
        
        # 验证密钥正确性
        test_msg = random.randint(2, N-1)
        cipher = pow(test_msg, e, N)
        decrypted = pow(cipher, d_recovered, N)
        print(f"  加解密测试 = {'✓ 通过' if test_msg == decrypted else '✗ 失败'}")
        
    else:
        print(f"✗ 攻击失败 - 未能恢复私钥")
    
    total_time = time.time() - total_start
    print(f"\n总耗时: {total_time:.3f} 秒")
    print(f"攻击耗时: {attack_time:.3f} 秒")
    print("=" * 80)
    
    return x_recovered is not None


# ============================================================================
# 主程序
# ============================================================================

def batch_experiments():
    """
    批量实验：测试不同参数组合
    """
    print("\n" + "=" * 80)
    print("批量实验 - 测试不同参数组合")
    print("=" * 80)

    experiments = [
        # (bit_length, r, s, delta, exposure_type, m, t, description)
        (64, 2, 1, 0.6, "MSB", 2, 1, "高泄露率 MSB (60%)"),
        (64, 2, 1, 0.5, "MSB", 3, 1, "中等泄露 MSB (50%, m=3)"),
        (64, 1, 1, 0.5, "MSB", 2, 1, "标准 RSA (p*q, 50%)"),
        (64, 2, 2, 0.6, "MSB", 2, 1, "对称幂次 (p^2*q^2, 60%)"),
        (48, 2, 1, 0.5, "LSB", 2, 1, "LSB 泄露 (48位素数)"),
    ]

    results = []

    for i, (bl, r, s, delta, exp_type, m, t, desc) in enumerate(experiments, 1):
        print(f"\n{'='*80}")
        print(f"实验 {i}/{len(experiments)}: {desc}")
        print(f"参数: bit_length={bl}, r={r}, s={s}, δ={delta}, type={exp_type}, m={m}, t={t}")
        print(f"{'='*80}")

        try:
            success = attack_partial_key_exposure(bl, r, s, delta, exp_type, m, t)
            results.append((desc, success))
        except Exception as e:
            print(f"✗ 实验失败: {e}")
            results.append((desc, False))

    # 汇总结果
    print("\n" + "=" * 80)
    print("实验汇总")
    print("=" * 80)
    for desc, success in results:
        status = "✓ 成功" if success else "✗ 失败"
        print(f"{status:8} | {desc}")

    success_rate = sum(1 for _, s in results if s) / len(results) * 100
    print(f"\n总成功率: {success_rate:.1f}% ({sum(1 for _, s in results if s)}/{len(results)})")
    print("=" * 80)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("广义 RSA 部分私钥泄露攻击演示")
    print("基于 Coppersmith 方法和格约简")
    print("=" * 80)

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        # 批量实验模式
        batch_experiments()
    else:
        # 单次演示模式 (快速演示参数)
        print("\n提示: 使用 'python partial_key_exposure_attack.py batch' 运行批量实验")
        print("\n" + "=" * 80)
        print("快速演示: N = p^2 * q, δ=0.6 (高泄露率), MSB")
        print("=" * 80)

        attack_partial_key_exposure(
            bit_length=64,    # 64位素数 (约128位N) - 确保几秒内完成
            r=2,              # p^2
            s=1,              # q^1
            delta=0.6,        # 泄露60%的位 (高成功率)
            exposure_type="MSB",
            m=3,              # 格参数 (平衡速度和成功率)
            t=1
        )

        print("\n" + "=" * 80)
        print("演示完成!")
        print("=" * 80)

