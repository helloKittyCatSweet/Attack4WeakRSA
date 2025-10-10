#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Partial Key Exposure Attack on RSA with Moduli N = p^r * q^s
纯 Python 实现（不依赖 SageMath）

使用 numpy 和 sympy 实现格约简和多项式求解
"""

import time
import random
import numpy as np
from sympy import symbols, Poly, ZZ, solve, gcd as sympy_gcd
from sympy.ntheory import isprime, nextprime
from Crypto.Util.number import getPrime, inverse, GCD

# ============================================================================
# 工具函数
# ============================================================================

def generate_rsa_generalized(bit_length, r, s):
    """
    生成广义 RSA 参数 N = p^r * q^s
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
    """
    d_bits = d.bit_length()
    known_bits = int(d_bits * delta)
    
    print(f"\n[*] 创建部分私钥泄露 (δ={delta}, type={exposure_type})")
    print(f"    d 总位长 = {d_bits} bits")
    print(f"    已知位数 = {known_bits} bits")
    print(f"    未知位数 = {d_bits - known_bits} bits")
    
    if exposure_type == "MSB":
        shift = d_bits - known_bits
        d0 = (d >> shift) << shift
        x = d - d0
        X = 2 ** shift
    else:  # LSB
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
# 简化的 LLL 算法实现
# ============================================================================

def gram_schmidt(B):
    """
    Gram-Schmidt 正交化
    """
    B = np.array(B, dtype=np.float64)
    n, m = B.shape
    B_star = np.zeros_like(B)
    mu = np.zeros((n, n))
    
    for i in range(n):
        B_star[i] = B[i].copy()
        for j in range(i):
            mu[i, j] = np.dot(B[i], B_star[j]) / np.dot(B_star[j], B_star[j])
            B_star[i] -= mu[i, j] * B_star[j]
    
    return B_star, mu


def lll_reduction(B, delta=0.75):
    """
    简化的 LLL 格约简算法
    
    参数:
        B: 格基矩阵 (行向量)
        delta: LLL 参数 (通常 0.75)
    """
    B = np.array(B, dtype=np.float64)
    n, m = B.shape
    
    k = 1
    while k < n:
        # Gram-Schmidt 正交化
        B_star, mu = gram_schmidt(B)
        
        # Size reduction
        for j in range(k - 1, -1, -1):
            if abs(mu[k, j]) > 0.5:
                q = round(mu[k, j])
                B[k] -= q * B[j]
                B_star, mu = gram_schmidt(B)
        
        # Lovász 条件检查
        if np.dot(B_star[k], B_star[k]) >= (delta - mu[k, k-1]**2) * np.dot(B_star[k-1], B_star[k-1]):
            k += 1
        else:
            # 交换
            B[[k, k-1]] = B[[k-1, k]]
            k = max(k - 1, 1)
    
    return B.astype(np.int64)


# ============================================================================
# Coppersmith 攻击核心
# ============================================================================

def coppersmith_attack_simple(N, e, d0, X, M, m=2):
    """
    简化的 Coppersmith 攻击（单变量）
    
    使用小参数以确保快速执行
    """
    print(f"\n[*] 开始 Coppersmith 格攻击")
    print(f"    格参数: m={m}")
    
    # 基本多项式 f(x) = e*x + (e*d0 - 1)
    C = e * d0 - 1
    
    print(f"    基本多项式: f(x) = {e}*x + {C}")
    print(f"    模 M = {M}")
    
    # 构造格基矩阵
    # 使用简化的构造：x^i * f(x)^j * M^(m-j)
    polynomials = []
    
    # 收集多项式系数
    for j in range(m):
        for i in range(m - j):
            # 计算 x^i * f(x)^j * M^(m-j) 的系数
            # f(x)^j = (e*x + C)^j
            coeffs = [0] * (i + j + 1)
            
            # 计算 (e*x + C)^j 的系数
            for k in range(j + 1):
                binom_coeff = 1
                for t in range(k):
                    binom_coeff = binom_coeff * (j - t) // (t + 1)
                coeffs[i + k] = binom_coeff * (e ** k) * (C ** (j - k)) * (M ** (m - j))
            
            polynomials.append(coeffs)
    
    # 构造格基矩阵
    n = len(polynomials)
    max_degree = max(len(p) for p in polynomials)

    print(f"    格维度: {n} x {max_degree}")

    # 创建矩阵并进行缩放（使用 Python 对象数组避免溢出）
    L_big = [[0 for _ in range(max_degree)] for _ in range(n)]

    for i, poly in enumerate(polynomials):
        for j, coeff in enumerate(poly):
            # 用 X 缩放
            L_big[i][j] = coeff * (X ** j)

    # 找到最大值并进行归一化
    max_val = max(max(abs(val) for val in row) for row in L_big)

    # 计算缩放因子
    if max_val > 1e15:
        scale = int(max_val / 1e12)
        print(f"    警告: 矩阵元素过大，缩放因子 = {scale}")
    else:
        scale = 1

    # 转换为 numpy 数组
    L = np.zeros((n, max_degree), dtype=np.float64)
    for i in range(n):
        for j in range(max_degree):
            L[i, j] = float(L_big[i][j] // scale)
    
    # LLL 格约简
    print(f"    开始 LLL 格约简...")
    start_time = time.time()
    
    try:
        L_reduced = lll_reduction(L)
        lll_time = time.time() - start_time
        print(f"    LLL 完成，耗时 {lll_time:.3f} 秒")
    except Exception as ex:
        print(f"    LLL 失败: {ex}")
        return None

    # 从短向量重构多项式并求根
    print(f"    从短向量重构多项式...")

    x_sym = symbols('x')

    for i in range(min(n, 3)):
        # 重构多项式（考虑缩放）
        coeffs = []
        for j in range(max_degree):
            scaled_val = int(L_reduced[i, j]) * scale
            if X ** j != 0:
                coeffs.append(scaled_val // (X ** j))
            else:
                coeffs.append(scaled_val)
        
        # 构造 sympy 多项式
        poly_expr = sum(c * (x_sym ** idx) for idx, c in enumerate(coeffs) if c != 0)
        
        if poly_expr == 0:
            continue
        
        try:
            # 求整数根
            roots = solve(poly_expr, x_sym)
            
            for root in roots:
                if root.is_integer and 0 < int(root) < X:
                    root_val = int(root)
                    print(f"    ✓ 找到候选根: x = {root_val}")
                    
                    # 验证
                    if (e * (d0 + root_val) - 1) % M == 0:
                        print(f"    ✓ 验证成功!")
                        return root_val
        except Exception as ex:
            continue
    
    print(f"    ✗ 未找到有效根")
    return None


# ============================================================================
# 暴力搜索（作为对比/备用）
# ============================================================================

def brute_force_search(N, e, d0, X, M, max_attempts=100000):
    """
    暴力搜索（仅用于小 X 的情况）
    """
    print(f"\n[*] 暴力搜索 (X={X}, max_attempts={max_attempts})")
    
    if X > max_attempts:
        print(f"    X 太大，跳过暴力搜索")
        return None
    
    start_time = time.time()
    
    for x in range(1, min(int(X), max_attempts)):
        if (e * (d0 + x) - 1) % M == 0:
            elapsed = time.time() - start_time
            print(f"    ✓ 找到: x = {x} (耗时 {elapsed:.3f} 秒)")
            return x
    
    print(f"    ✗ 未找到")
    return None


# ============================================================================
# 主攻击流程
# ============================================================================

def attack_partial_key_exposure(bit_length=32, r=2, s=1, delta=0.6, 
                                 exposure_type="MSB", m=2, use_brute_force=True):
    """
    完整的部分私钥泄露攻击流程
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
    M = phi
    
    print(f"\n[*] 攻击配置")
    print(f"    模 M = φ(N)")
    print(f"    格参数: m={m}")
    
    # 步骤 4: 尝试 Coppersmith 攻击
    attack_start = time.time()
    x_recovered = coppersmith_attack_simple(N, e, d0, X, M, m)
    attack_time = time.time() - attack_start
    
    # 如果失败且 X 较小，尝试暴力搜索
    if x_recovered is None and use_brute_force and X < 1000000:
        print(f"\n[*] Coppersmith 失败，尝试暴力搜索...")
        x_recovered = brute_force_search(N, e, d0, X, M)
    
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
        test_msg = random.randint(2, min(N-1, 1000000))
        cipher = pow(test_msg, e, N)
        decrypted = pow(cipher, d_recovered, N)
        print(f"  加解密测试 = {'✓ 通过' if test_msg == decrypted else '✗ 失败'}")
        
    else:
        print(f"✗ 攻击失败 - 未能恢复私钥")
    
    total_time = time.time() - total_start
    print(f"\n总耗时: {total_time:.3f} 秒")
    print("=" * 80)
    
    return x_recovered is not None


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("广义 RSA 部分私钥泄露攻击演示 (纯 Python 版本)")
    print("基于 Coppersmith 方法和格约简")
    print("=" * 80)
    
    # 使用非常小的参数以确保快速执行（几秒内）
    print("\n快速演示: 使用小参数确保快速完成")
    print("=" * 80)
    
    attack_partial_key_exposure(
        bit_length=32,    # 32位素数（非常小，仅用于演示）
        r=2,              # p^2
        s=1,              # q^1
        delta=0.7,        # 泄露70%的位（高泄露率）
        exposure_type="MSB",
        m=2,              # 小格参数
        use_brute_force=True  # 允许暴力搜索作为备用
    )
    
    print("\n" + "=" * 80)
    print("演示完成!")
    print("=" * 80)

