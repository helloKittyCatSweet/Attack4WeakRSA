#!/usr/bin/env python3
"""
Comprehensive Wiener Attack Demonstration
综合维纳攻击演示

展示论文 "A New Boundary of Minimum Private Key on Wiener Attack Against RSA Algorithm" 的实现
"""

from Crypto.Util.number import getPrime, inverse, GCD
from wiener_attack import WienerAttack, BunderTonienAttack, NewBoundaryAttack
from visualizer import AttackVisualizer
import time


class WienerDemo:
    """维纳攻击综合演示"""
    
    def __init__(self):
        self.wiener = WienerAttack()
        self.bunder_tonien = BunderTonienAttack()
        self.new_boundary = NewBoundaryAttack()
        self.viz = AttackVisualizer()
    
    def demo_1_basic_attack(self):
        """演示1: 基本Wiener攻击"""
        self.viz.print_header("演示1: 基本Wiener攻击")
        
        print("\n生成易受攻击的RSA密钥...")
        print("策略: 使用非常小的私钥 d")
        
        # 生成密钥
        p = getPrime(256)
        q = getPrime(256)
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # 使用小的d
        d = 12345
        while GCD(d, phi) != 1:
            d += 2
        
        e = inverse(d, phi)
        
        print(f"\nRSA参数:")
        print(f"  N 比特长度: {n.bit_length()}")
        print(f"  d = {d} ({d.bit_length()} bits)")
        print(f"  e = {e}")
        
        # 检查边界
        wiener_bound = self.wiener.get_boundary(n)
        print(f"\nWiener边界: {wiener_bound:.2e}")
        print(f"d < 边界: {'✓' if d < wiener_bound else '✗'}")
        
        # 执行攻击
        print("\n执行Wiener攻击...")
        start = time.perf_counter()
        recovered_d = self.wiener.attack(e, n)
        elapsed = time.perf_counter() - start
        
        # 显示结果
        if recovered_d == d:
            print(f"✓ 攻击成功! 耗时: {elapsed*1000:.3f} ms")
            print(f"  恢复的私钥: {recovered_d}")
            
            # 验证加密解密
            msg = 123456789
            cipher = pow(msg, e, n)
            decrypted = pow(cipher, recovered_d, n)
            print(f"  加密解密验证: {'✓' if decrypted == msg else '✗'}")
        else:
            print(f"✗ 攻击失败")
    
    def demo_2_boundary_comparison(self):
        """演示2: 三种攻击方法的边界对比"""
        self.viz.print_header("演示2: 三种攻击方法的边界对比")
        
        print("\n根据论文，三种攻击方法的边界条件为:")
        print("  1. Wiener (1990):      d < N^0.25 / 3")
        print("  2. Bunder-Tonien (2017): d < 2√(2N)")
        print("  3. New Boundary (2023):  d < √(8.24264N)")
        
        # 测试不同大小的N
        test_sizes = [256, 512, 1024, 2048]
        
        print(f"\n{'N位长':<10} {'Wiener':<20} {'Bunder-Tonien':<20} {'New Boundary':<20}")
        print("-" * 75)
        
        for bits in test_sizes:
            p = getPrime(bits // 2)
            q = getPrime(bits // 2)
            n = p * q
            
            w_bound = self.wiener.get_boundary(n)
            bt_bound = self.bunder_tonien.get_boundary(n)
            new_bound = self.new_boundary.get_boundary(n)
            
            print(f"{n.bit_length():<10} {w_bound:<20.2e} {bt_bound:<20.2e} {new_bound:<20.2e}")
        
        print("\n关键观察:")
        print("  • Bunder-Tonien的边界远大于Wiener")
        print("  • 新边界略大于Bunder-Tonien (约1.02倍)")
        print("  • 边界越大，可攻击的私钥范围越广")
    
    def demo_3_attack_comparison(self):
        """演示3: 三种攻击方法的实际对比"""
        self.viz.print_header("演示3: 三种攻击方法实际对比")
        
        print("\n生成测试密钥...")
        
        # 生成密钥
        p = getPrime(256)
        q = getPrime(256)
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # 使用小d
        d = 65537
        while GCD(d, phi) != 1:
            d += 2
        
        e = inverse(d, phi)
        
        print(f"N 比特长度: {n.bit_length()}")
        print(f"d = {d}")
        
        # 检查各种边界
        print("\n边界检查:")
        w_bound = self.wiener.get_boundary(n)
        bt_bound = self.bunder_tonien.get_boundary(n)
        new_bound = self.new_boundary.get_boundary(n)
        
        print(f"  Wiener边界:      {w_bound:.2e} - {'✓ 可攻击' if d < w_bound else '✗ 不可攻击'}")
        print(f"  Bunder-Tonien:   {bt_bound:.2e} - {'✓ 可攻击' if d < bt_bound else '✗ 不可攻击'}")
        print(f"  New Boundary:    {new_bound:.2e} - {'✓ 可攻击' if d < new_bound else '✗ 不可攻击'}")
        
        # 执行三种攻击
        print("\n执行攻击:")
        
        methods = [
            ("Wiener", self.wiener),
            ("Bunder-Tonien", self.bunder_tonien),
            ("New Boundary", self.new_boundary)
        ]
        
        for name, attacker in methods:
            start = time.perf_counter()
            recovered = attacker.attack(e, n)
            elapsed = time.perf_counter() - start
            
            success = recovered == d
            print(f"  {name:<20} {'✓ 成功' if success else '✗ 失败':<15} {elapsed*1000:>8.3f} ms")
    
    def demo_4_performance_benchmark(self):
        """演示4: 性能基准测试（复现论文结果）"""
        self.viz.print_header("演示4: 性能基准测试")
        
        print("\n论文中的实验结果 (Intel i5-8265U + 4GB RAM):")
        print("  1024-bit: 0.052s")
        print("  2048-bit: 0.152s")
        print("  4096-bit: 0.75s")
        print("  8192-bit: 4.42s")
        
        print("\n本机测试结果:")
        print(f"{'RSA位长':<15} {'耗时(秒)':<15} {'耗时(毫秒)':<15} {'状态':<10}")
        print("-" * 60)
        
        test_configs = [
            (256, 12345),
            (512, 65537),
            (1024, 65537),
        ]
        
        for bits, d_value in test_configs:
            p = getPrime(bits // 2)
            q = getPrime(bits // 2)
            n = p * q
            phi = (p - 1) * (q - 1)
            
            d = d_value
            while GCD(d, phi) != 1:
                d += 2
            
            e = inverse(d, phi)
            
            # 确保满足Wiener条件
            if d < self.wiener.get_boundary(n):
                start = time.perf_counter()
                recovered = self.wiener.attack(e, n)
                elapsed = time.perf_counter() - start
                
                success = recovered == d
                status = '✓' if success else '✗'
                print(f"{n.bit_length():<15} {elapsed:<15.3f} {elapsed*1000:<15.2f} {status:<10}")
            else:
                print(f"{n.bit_length():<15} {'N/A':<15} {'N/A':<15} {'跳过':<10}")
        
        print("\n注意: 时间复杂度为 O(log N)，与密钥长度呈对数关系")
    
    def demo_5_theoretical_analysis(self):
        """演示5: 理论分析"""
        self.viz.print_theoretical_analysis()
    
    def demo_6_security_recommendations(self):
        """演示6: 安全建议"""
        self.viz.print_security_recommendations()
    
    def run_all_demos(self):
        """运行所有演示"""
        print("\n" + "="*70)
        print("Wiener攻击及其改进 - 综合演示".center(70))
        print("基于论文: A New Boundary of Minimum Private Key".center(70))
        print("on Wiener Attack Against RSA Algorithm (2023)".center(70))
        print("="*70)
        
        demos = [
            self.demo_1_basic_attack,
            self.demo_2_boundary_comparison,
            self.demo_3_attack_comparison,
            self.demo_4_performance_benchmark,
            self.demo_5_theoretical_analysis,
            self.demo_6_security_recommendations
        ]
        
        for i, demo in enumerate(demos, 1):
            print(f"\n\n")
            demo()
            if i < len(demos):
                input("\n按Enter继续下一个演示...")
        
        print("\n" + "="*70)
        print("所有演示完成!".center(70))
        print("="*70)


def main():
    """主函数"""
    demo = WienerDemo()
    demo.run_all_demos()


if __name__ == "__main__":
    main()

