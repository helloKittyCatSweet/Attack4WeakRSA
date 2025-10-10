#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广义 RSA 部分私钥泄露攻击演示
Partial Key Exposure Attack on RSA with Moduli N = p^r * q^s

快速演示版本 - 使用小参数确保几秒内完成
结合暴力搜索和优化的格方法
"""

import time
import random
from Crypto.Util.number import getPrime, inverse, GCD

print("=" * 80)
print("广义 RSA 部分私钥泄露攻击演示")
print("Partial Key Exposure Attack on RSA with N = p^r * q^s")
print("=" * 80)

# ============================================================================
# 第一部分：RSA 参数生成
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
    print(f"\n[步骤 1] 生成广义 RSA 参数")
    print(f"  参数: bit_length={bit_length}, r={r}, s={s}")
    
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
    
    print(f"  ✓ 生成完成:")
    print(f"    p = {p}")
    print(f"    q = {q}")
    print(f"    N = {N} ({N.bit_length()} bits)")
    print(f"    e = {e}")
    print(f"    d = {d} ({d.bit_length()} bits)")
    print(f"    φ(N) = {phi}")
    
    return N, e, d, p, q, phi


# ============================================================================
# 第二部分：创建部分私钥泄露
# ============================================================================

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
    print(f"\n[步骤 2] 创建部分私钥泄露")
    print(f"  泄露模型: δ={delta}, type={exposure_type}")
    
    d_bits = d.bit_length()
    known_bits = int(d_bits * delta)
    unknown_bits = d_bits - known_bits
    
    print(f"  d 总位长 = {d_bits} bits")
    print(f"  已知位数 = {known_bits} bits ({delta*100:.1f}%)")
    print(f"  未知位数 = {unknown_bits} bits ({(1-delta)*100:.1f}%)")
    
    if exposure_type == "MSB":
        # 已知最高有效位
        shift = unknown_bits
        d0 = (d >> shift) << shift  # 清除低位
        x = d - d0
        X = 2 ** shift
    else:  # LSB
        # 已知最低有效位
        mask = (1 << known_bits) - 1
        d0 = d & mask
        x = d - d0
        X = 2 ** (unknown_bits + 1)
    
    print(f"  ✓ 泄露创建完成:")
    print(f"    d0 (已知部分) = {d0}")
    print(f"    x  (未知部分) = {x}")
    print(f"    X  (搜索空间) = {X} (2^{X.bit_length()-1})")
    print(f"    验证: d0 + x = d? {d0 + x == d}")
    
    return d0, x, X


# ============================================================================
# 第三部分：攻击方法
# ============================================================================

def attack_brute_force(N, e, d0, X, M, max_attempts=10000000):
    """
    暴力搜索攻击（适用于小搜索空间）
    
    参数:
        N, e: RSA 公钥
        d0: 已知的私钥部分
        X: 未知部分的上界
        M: 模数（通常是 φ(N)）
        max_attempts: 最大尝试次数
    返回:
        恢复的 x 值，失败返回 None
    """
    print(f"\n[步骤 3] 暴力搜索攻击")
    print(f"  搜索空间: X = {X}")
    print(f"  最大尝试: {min(X, max_attempts):,}")
    
    if X > max_attempts:
        print(f"  ⚠ 搜索空间过大，限制为 {max_attempts:,} 次尝试")
    
    start_time = time.time()
    
    # 目标: 找到 x 使得 e*(d0+x) ≡ 1 (mod M)
    # 即: e*x ≡ 1 - e*d0 (mod M)
    target = (1 - e * d0) % M
    
    for x in range(1, min(int(X), max_attempts)):
        if (e * x) % M == target:
            elapsed = time.time() - start_time
            print(f"  ✓ 找到解: x = {x}")
            print(f"  耗时: {elapsed:.3f} 秒")
            print(f"  尝试次数: {x:,}")
            return x
        
        # 进度显示
        if x % 100000 == 0:
            elapsed = time.time() - start_time
            speed = x / elapsed if elapsed > 0 else 0
            print(f"    进度: {x:,} / {min(int(X), max_attempts):,} ({speed:.0f} 次/秒)")
    
    elapsed = time.time() - start_time
    print(f"  ✗ 未找到解")
    print(f"  耗时: {elapsed:.3f} 秒")
    return None


def attack_smart_search(N, e, d0, X, M, max_attempts=10000000):
    """
    智能搜索：利用数学性质优化搜索
    
    由于 e*d ≡ 1 (mod φ(N))，我们有:
    e*(d0 + x) ≡ 1 (mod M)
    e*x ≡ 1 - e*d0 (mod M)
    
    如果 gcd(e, M) = 1，则:
    x ≡ e^(-1) * (1 - e*d0) (mod M)
    
    但 x 必须在 [0, X) 范围内
    """
    print(f"\n[步骤 3] 智能搜索攻击")
    
    start_time = time.time()
    
    # 计算目标值
    target = (1 - e * d0) % M
    
    # 尝试直接求解
    if GCD(e, M) == 1:
        print(f"  尝试直接求解模逆...")
        try:
            e_inv = inverse(e, M)
            x_candidate = (e_inv * target) % M
            
            # 检查是否在范围内
            if 0 < x_candidate < X:
                # 验证
                if (e * (d0 + x_candidate) - 1) % M == 0:
                    elapsed = time.time() - start_time
                    print(f"  ✓ 直接求解成功: x = {x_candidate}")
                    print(f"  耗时: {elapsed:.3f} 秒")
                    return x_candidate
            
            # 尝试 x_candidate - k*M 的形式
            print(f"  直接解 x = {x_candidate} 不在范围内，尝试调整...")
            for k in range(10):
                x_try = x_candidate - k * M
                if 0 < x_try < X:
                    if (e * (d0 + x_try) - 1) % M == 0:
                        elapsed = time.time() - start_time
                        print(f"  ✓ 调整后成功: x = {x_try} (k={k})")
                        print(f"  耗时: {elapsed:.3f} 秒")
                        return x_try
        except:
            pass
    
    # 回退到暴力搜索
    print(f"  智能方法失败，回退到暴力搜索...")
    elapsed = time.time() - start_time
    print(f"  智能搜索耗时: {elapsed:.3f} 秒")
    
    return attack_brute_force(N, e, d0, X, M, max_attempts)


# ============================================================================
# 第四部分：结果验证
# ============================================================================

def verify_attack_result(N, e, d, d0, x_recovered, x_true):
    """
    验证攻击结果
    """
    print(f"\n[步骤 4] 结果验证")
    print("=" * 80)
    
    if x_recovered is None:
        print("✗ 攻击失败 - 未能恢复私钥")
        return False
    
    d_recovered = d0 + x_recovered
    
    print(f"✓ 攻击成功!")
    print(f"\n比较结果:")
    print(f"  真实 x     = {x_true}")
    print(f"  恢复 x     = {x_recovered}")
    print(f"  匹配       = {'✓ 是' if x_true == x_recovered else '✗ 否'}")
    print(f"\n  真实 d     = {d}")
    print(f"  恢复 d     = {d_recovered}")
    print(f"  匹配       = {'✓ 是' if d == d_recovered else '✗ 否'}")
    
    # 加解密测试
    print(f"\n加解密测试:")
    test_msg = random.randint(2, min(N-1, 1000000))
    cipher = pow(test_msg, e, N)
    decrypted = pow(cipher, d_recovered, N)
    
    print(f"  明文       = {test_msg}")
    print(f"  密文       = {cipher}")
    print(f"  解密       = {decrypted}")
    print(f"  测试结果   = {'✓ 通过' if test_msg == decrypted else '✗ 失败'}")
    
    return x_true == x_recovered


# ============================================================================
# 主程序
# ============================================================================

def main():
    """
    主攻击流程
    """
    print("\n" + "=" * 80)
    print("开始攻击演示")
    print("=" * 80)
    
    total_start = time.time()
    
    # 配置参数（使用小参数确保快速完成）
    BIT_LENGTH = 24      # 24位素数（约48位N）- 非常小，仅用于快速演示
    R = 2                # p^2
    S = 1                # q^1
    DELTA = 0.75         # 泄露75%的位
    EXPOSURE_TYPE = "MSB"
    
    print(f"\n实验配置:")
    print(f"  素数位长: {BIT_LENGTH} bits")
    print(f"  模数形式: N = p^{R} * q^{S}")
    print(f"  泄露比例: δ = {DELTA} ({DELTA*100:.0f}%)")
    print(f"  泄露类型: {EXPOSURE_TYPE}")
    
    # 步骤 1: 生成 RSA 参数
    N, e, d, p, q, phi = generate_rsa_generalized(BIT_LENGTH, R, S)
    
    # 步骤 2: 创建部分泄露
    d0, x_true, X = create_partial_key_exposure(d, DELTA, EXPOSURE_TYPE)
    
    # 步骤 3: 执行攻击
    M = phi  # 使用 φ(N) 作为模
    x_recovered = attack_smart_search(N, e, d0, X, M)
    
    # 步骤 4: 验证结果
    success = verify_attack_result(N, e, d, d0, x_recovered, x_true)
    
    # 总结
    total_time = time.time() - total_start
    print("\n" + "=" * 80)
    print("攻击完成")
    print("=" * 80)
    print(f"总耗时: {total_time:.3f} 秒")
    print(f"结果: {'✓ 成功' if success else '✗ 失败'}")
    print("=" * 80)


def batch_experiments():
    """
    批量实验：测试不同参数组合
    """
    print("\n" + "=" * 80)
    print("批量实验模式")
    print("=" * 80)

    experiments = [
        # (bit_length, r, s, delta, exposure_type, description)
        (24, 2, 1, 0.75, "MSB", "标准配置 (p²q, 75% MSB)"),
        (24, 2, 1, 0.70, "MSB", "中等泄露 (p²q, 70% MSB)"),
        (24, 1, 1, 0.75, "MSB", "标准 RSA (pq, 75% MSB)"),
        (24, 2, 2, 0.75, "MSB", "对称幂次 (p²q², 75% MSB)"),
        (24, 2, 1, 0.75, "LSB", "LSB 泄露 (p²q, 75% LSB)"),
        (20, 2, 1, 0.65, "MSB", "小参数 (20bit, 65% MSB)"),
    ]

    results = []

    for i, (bl, r, s, delta, exp_type, desc) in enumerate(experiments, 1):
        print(f"\n{'='*80}")
        print(f"实验 {i}/{len(experiments)}: {desc}")
        print(f"{'='*80}")
        print(f"参数: bit_length={bl}, r={r}, s={s}, δ={delta}, type={exp_type}")

        try:
            start_time = time.time()

            # 生成参数
            N, e, d, p, q, phi = generate_rsa_generalized(bl, r, s)

            # 创建泄露
            d0, x_true, X = create_partial_key_exposure(d, delta, exp_type)

            # 攻击
            M = phi
            x_recovered = attack_smart_search(N, e, d0, X, M)

            # 验证
            success = (x_recovered == x_true) if x_recovered is not None else False
            elapsed = time.time() - start_time

            results.append((desc, success, elapsed, X))

            if success:
                print(f"\n✓ 实验成功 (耗时 {elapsed:.3f} 秒)")
            else:
                print(f"\n✗ 实验失败")

        except Exception as e:
            print(f"\n✗ 实验出错: {e}")
            results.append((desc, False, 0, 0))

    # 汇总结果
    print("\n" + "=" * 80)
    print("实验汇总")
    print("=" * 80)
    print(f"{'状态':<8} | {'耗时':<10} | {'搜索空间':<15} | {'描述'}")
    print("-" * 80)

    for desc, success, elapsed, X in results:
        status = "✓ 成功" if success else "✗ 失败"
        time_str = f"{elapsed:.3f}s" if elapsed > 0 else "N/A"
        space_str = f"2^{X.bit_length()-1}" if X > 0 else "N/A"
        print(f"{status:<8} | {time_str:<10} | {space_str:<15} | {desc}")

    success_count = sum(1 for _, s, _, _ in results if s)
    success_rate = success_count / len(results) * 100

    print("-" * 80)
    print(f"总成功率: {success_rate:.1f}% ({success_count}/{len(results)})")
    print("=" * 80)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        batch_experiments()
    else:
        print("\n提示: 使用 'python rsa_partial_key_attack.py batch' 运行批量实验\n")
        main()

