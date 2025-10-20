#!/usr/bin/env python3
"""
Simple test for Wiener attack
简单的维纳攻击测试
"""

from Crypto.Util.number import getPrime, inverse, GCD
from wiener_attack import WienerAttack, BunderTonienAttack, NewBoundaryAttack
import time


def test_wiener_basic():
    """测试基本的Wiener攻击"""
    print("="*70)
    print("基本Wiener攻击测试")
    print("="*70)
    
    # 生成一个非常小的d来确保攻击成功
    print("\n[1] 生成弱RSA密钥...")
    
    # 使用较小的素数
    p = getPrime(256)
    q = getPrime(256)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # 选择一个非常小的d
    d = 12345
    while GCD(d, phi) != 1:
        d += 2
    
    e = inverse(d, phi)
    
    print(f"  N = {n}")
    print(f"  N 比特长度: {n.bit_length()}")
    print(f"  e = {e}")
    print(f"  d = {d}")
    print(f"  d 比特长度: {d.bit_length()}")
    
    # 检查边界
    wiener_bound = pow(n, 0.25) / 3
    print(f"\n  Wiener边界: {wiener_bound:.2e}")
    print(f"  d < 边界: {d < wiener_bound}")
    
    # 执行攻击
    print("\n[2] 执行Wiener攻击...")
    attacker = WienerAttack()
    
    start = time.perf_counter()
    recovered_d = attacker.attack(e, n)
    elapsed = time.perf_counter() - start
    
    # 验证结果
    print("\n[3] 验证结果...")
    if recovered_d is not None:
        print(f"  ✓ 攻击成功!")
        print(f"  原始私钥: {d}")
        print(f"  恢复私钥: {recovered_d}")
        print(f"  匹配: {'✓' if d == recovered_d else '✗'}")
        print(f"  耗时: {elapsed*1000:.3f} ms")
        
        # 测试加密解密
        message = 123456789
        ciphertext = pow(message, e, n)
        decrypted = pow(ciphertext, recovered_d, n)
        print(f"\n  加密解密测试: {'✓' if decrypted == message else '✗'}")
    else:
        print(f"  ✗ 攻击失败")
        print(f"  耗时: {elapsed*1000:.3f} ms")


def test_different_key_sizes():
    """测试不同密钥大小"""
    print("\n" + "="*70)
    print("不同密钥大小测试")
    print("="*70)
    
    key_sizes = [256, 512, 1024]
    
    for bits in key_sizes:
        print(f"\n测试 {bits}-bit RSA...")
        
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # 使用固定的小d
        d = 65537
        while GCD(d, phi) != 1:
            d += 2
        
        e = inverse(d, phi)
        
        print(f"  N 比特长度: {n.bit_length()}")
        print(f"  d: {d}")
        
        # 检查是否满足Wiener条件
        wiener_bound = pow(n, 0.25) / 3
        vulnerable = d < wiener_bound
        print(f"  满足Wiener条件: {vulnerable}")
        
        if vulnerable:
            attacker = WienerAttack()
            start = time.perf_counter()
            recovered_d = attacker.attack(e, n)
            elapsed = time.perf_counter() - start
            
            success = recovered_d == d
            print(f"  攻击结果: {'✓ 成功' if success else '✗ 失败'}")
            print(f"  耗时: {elapsed*1000:.3f} ms")
        else:
            print(f"  跳过攻击（不满足条件）")


def test_boundary_comparison():
    """测试三种攻击方法的边界"""
    print("\n" + "="*70)
    print("边界对比测试")
    print("="*70)
    
    # 生成密钥
    p = getPrime(256)
    q = getPrime(256)
    n = p * q
    
    wiener = WienerAttack()
    bunder_tonien = BunderTonienAttack()
    new_boundary = NewBoundaryAttack()
    
    wiener_bound = wiener.get_boundary(n)
    bt_bound = bunder_tonien.get_boundary(n)
    new_bound = new_boundary.get_boundary(n)
    
    print(f"\nN = {n}")
    print(f"N 比特长度: {n.bit_length()}")
    print(f"\n边界对比:")
    print(f"  Wiener:         {wiener_bound:.2e}")
    print(f"  Bunder-Tonien:  {bt_bound:.2e}")
    print(f"  New Boundary:   {new_bound:.2e}")
    print(f"\n提升倍数:")
    print(f"  BT vs Wiener:   {bt_bound/wiener_bound:.2f}x")
    print(f"  New vs Wiener:  {new_bound/wiener_bound:.2f}x")
    print(f"  New vs BT:      {new_bound/bt_bound:.2f}x")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("Wiener攻击简单测试")
    print("="*70)
    
    # 测试1: 基本Wiener攻击
    test_wiener_basic()
    
    # 测试2: 不同密钥大小
    test_different_key_sizes()
    
    # 测试3: 边界对比
    test_boundary_comparison()
    
    print("\n" + "="*70)
    print("测试完成")
    print("="*70)


if __name__ == "__main__":
    main()

