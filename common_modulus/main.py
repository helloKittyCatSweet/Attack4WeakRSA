#!/usr/bin/env python3
"""
Common Modulus Attack - Main Program
同模数攻击主程序

支持多种运行模式:
1. paper - 复现论文示例
2. demo - 演示攻击过程
3. test - 运行测试套件
4. custom - 自定义参数攻击
"""

import argparse
from Crypto.Util.number import getPrime, inverse, GCD
from common_modulus_attack import CommonModulusAttack, ECCRSACommonModulusAttack
from config import TEST_CONFIGS, ECC_PARAMS
import time


def mode_paper():
    """模式1: 复现论文示例"""
    from paper_example import main as paper_main
    paper_main()


def mode_demo():
    """模式2: 演示攻击过程"""
    print("\n" + "="*70)
    print("同模数攻击演示")
    print("="*70)
    
    print("\n场景: 两个用户使用相同的RSA模数N，但使用不同的公钥指数")
    print("      攻击者截获了同一消息的两个密文")
    
    # 生成RSA参数
    print("\n[1] 生成RSA参数...")
    p = getPrime(256)
    q = getPrime(256)
    N = p * q
    phi = (p - 1) * (q - 1)
    
    # 选择两个互素的公钥指数
    e1 = 3
    e2 = 5

    # 确保e1, e2与phi互素
    while GCD(e1, phi) != 1:
        e1 += 2

    # 确保e2与phi互素且e2 != e1
    while GCD(e2, phi) != 1 or e2 == e1:
        e2 += 2
    
    print(f"  N = {N}")
    print(f"  N 比特长度: {N.bit_length()}")
    print(f"  e1 = {e1}")
    print(f"  e2 = {e2}")
    
    # 原始消息
    M = 123456789
    print(f"\n[2] 原始消息:")
    print(f"  M = {M}")
    
    # 生成两个密文
    print(f"\n[3] 用户1使用e1加密，用户2使用e2加密:")
    C1 = pow(M, e1, N)
    C2 = pow(M, e2, N)
    print(f"  C1 = M^{e1} mod N = {C1}")
    print(f"  C2 = M^{e2} mod N = {C2}")
    
    # 执行攻击
    print(f"\n[4] 攻击者执行同模数攻击...")
    attacker = CommonModulusAttack()
    
    start = time.perf_counter()
    recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=True)
    elapsed = time.perf_counter() - start
    
    # 验证
    print(f"\n[5] 攻击结果:")
    if recovered_M == M:
        print(f"  ✓ 攻击成功!")
        print(f"  原始消息: {M}")
        print(f"  恢复消息: {recovered_M}")
        print(f"  总耗时: {elapsed*1000:.3f} ms")
    else:
        print(f"  ✗ 攻击失败")


def mode_test():
    """模式3: 运行测试套件"""
    print("\n" + "="*70)
    print("同模数攻击测试套件")
    print("="*70)
    
    attacker = CommonModulusAttack()
    
    test_cases = [
        ("小型RSA (512-bit)", 512, 3, 5),
        ("中型RSA (1024-bit)", 1024, 7, 11),
        ("大型RSA (2048-bit)", 2048, 17, 257),
    ]
    
    results = []
    
    for name, bits, e1, e2 in test_cases:
        print(f"\n{'='*70}")
        print(f"测试: {name}")
        print(f"{'='*70}")
        
        # 生成密钥
        print(f"\n[1] 生成 {bits}-bit RSA密钥...")
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)
        N = p * q
        phi = (p - 1) * (q - 1)
        
        # 确保e1, e2与phi互素且互不相同
        while GCD(e1, phi) != 1:
            e1 += 2
        while GCD(e2, phi) != 1 or e2 == e1:
            e2 += 2
        
        print(f"  N 比特长度: {N.bit_length()}")
        print(f"  e1 = {e1}, e2 = {e2}")
        
        # 生成消息和密文
        M = 987654321
        C1 = pow(M, e1, N)
        C2 = pow(M, e2, N)
        
        print(f"\n[2] 执行攻击...")
        start = time.perf_counter()
        recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=False)
        elapsed = time.perf_counter() - start
        
        success = recovered_M == M
        
        print(f"  结果: {'✓ 成功' if success else '✗ 失败'}")
        print(f"  耗时: {elapsed*1000:.3f} ms")
        
        results.append((name, success, elapsed))
    
    # 总结
    print(f"\n{'='*70}")
    print("测试总结")
    print(f"{'='*70}")
    print(f"{'测试用例':<30} {'结果':<10} {'耗时(ms)':<15}")
    print("-" * 70)
    
    for name, success, elapsed in results:
        status = '✓ 成功' if success else '✗ 失败'
        print(f"{name:<30} {status:<10} {elapsed*1000:<15.3f}")
    
    success_count = sum(1 for _, s, _ in results if s)
    print(f"\n通过率: {success_count}/{len(results)} ({success_count/len(results)*100:.0f}%)")


def mode_custom(bits, e1, e2, message):
    """模式4: 自定义参数攻击"""
    print("\n" + "="*70)
    print("自定义参数攻击")
    print("="*70)
    
    print(f"\n[1] 参数:")
    print(f"  RSA位长: {bits}")
    print(f"  e1 = {e1}")
    print(f"  e2 = {e2}")
    print(f"  消息 = {message}")
    
    # 生成RSA密钥
    print(f"\n[2] 生成RSA密钥...")
    p = getPrime(bits // 2)
    q = getPrime(bits // 2)
    N = p * q
    phi = (p - 1) * (q - 1)
    
    # 检查e1, e2
    if GCD(e1, phi) != 1 or GCD(e2, phi) != 1:
        print(f"  ✗ 错误: e1或e2与φ(N)不互素")
        return
    
    if GCD(e1, e2) != 1:
        print(f"  ✗ 错误: e1和e2不互素，无法攻击")
        return
    
    print(f"  N 比特长度: {N.bit_length()}")
    
    # 加密
    print(f"\n[3] 加密消息...")
    C1 = pow(message, e1, N)
    C2 = pow(message, e2, N)
    
    # 攻击
    print(f"\n[4] 执行攻击...")
    attacker = CommonModulusAttack()
    recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=True)
    
    # 验证
    if recovered_M == message:
        print(f"\n✓ 攻击成功!")
    else:
        print(f"\n✗ 攻击失败")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Common Modulus Attack on RSA and ECC-RSA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --mode paper              # 复现论文示例
  python main.py --mode demo               # 演示攻击
  python main.py --mode test               # 运行测试
  python main.py --mode custom --bits 1024 --e1 3 --e2 5 --message 12345
        """
    )
    
    parser.add_argument('--mode', 
                       choices=['paper', 'demo', 'test', 'custom'],
                       default='demo',
                       help='运行模式')
    
    parser.add_argument('--bits',
                       type=int,
                       default=1024,
                       help='RSA密钥位长 (仅用于custom模式)')
    
    parser.add_argument('--e1',
                       type=int,
                       default=3,
                       help='第一个公钥指数 (仅用于custom模式)')
    
    parser.add_argument('--e2',
                       type=int,
                       default=5,
                       help='第二个公钥指数 (仅用于custom模式)')
    
    parser.add_argument('--message',
                       type=int,
                       default=123456789,
                       help='消息 (仅用于custom模式)')
    
    args = parser.parse_args()
    
    if args.mode == 'paper':
        mode_paper()
    elif args.mode == 'demo':
        mode_demo()
    elif args.mode == 'test':
        mode_test()
    elif args.mode == 'custom':
        mode_custom(args.bits, args.e1, args.e2, args.message)


if __name__ == "__main__":
    main()

