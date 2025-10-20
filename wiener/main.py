#!/usr/bin/env python3
"""
Wiener Attack and Improvements - Main Demonstration
维纳攻击及其改进版本 - 主演示程序

基于论文: "A New Boundary of Minimum Private Key on Wiener Attack Against RSA Algorithm" (2023)
"""

import argparse
import time
import math
from rsa_weak_key_generator import WeakRSAGenerator
from wiener_attack import WienerAttack, BunderTonienAttack, NewBoundaryAttack, AttackComparison
from config import DEFAULT_CONFIG, BENCHMARK_CONFIGS, PAPER_CONFIGS


class WienerAttackDemo:
    """维纳攻击演示主类"""
    
    def __init__(self):
        self.key_gen = WeakRSAGenerator()
        self.wiener = WienerAttack()
        self.bunder_tonien = BunderTonienAttack()
        self.new_boundary = NewBoundaryAttack()
        self.comparison = AttackComparison()
    
    def run_single_attack(self, bits=1024, attack_type="new_boundary"):
        """
        运行单次攻击演示
        
        Args:
            bits: RSA模数比特长度
            attack_type: 攻击类型 ("wiener", "bunder_tonien", "new_boundary")
        """
        print("="*70)
        print(f"维纳攻击演示 - {attack_type.upper()}")
        print("="*70)
        
        # 生成弱RSA密钥
        print(f"\n[1] 生成 {bits}-bit 弱RSA密钥...")
        n, e, d, p, q, boundary = self.key_gen.generate_by_boundary(bits, attack_type)
        
        print(f"  N = {n}")
        print(f"  e = {e}")
        print(f"  d = {d}")
        print(f"  p = {p}")
        print(f"  q = {q}")
        print(f"\n  N 比特长度: {n.bit_length()}")
        print(f"  d 比特长度: {d.bit_length()}")
        print(f"  理论边界: {boundary:.2e}")
        print(f"  d < 边界: {'✓' if d < boundary else '✗'}")
        
        # 检查脆弱性
        print(f"\n[2] 检查密钥脆弱性...")
        vuln = self.key_gen.check_vulnerability(n, d)
        self._print_vulnerability(vuln)
        
        # 执行攻击
        print(f"\n[3] 执行 {attack_type} 攻击...")
        
        if attack_type == "wiener":
            attacker = self.wiener
        elif attack_type == "bunder_tonien":
            attacker = self.bunder_tonien
        else:
            attacker = self.new_boundary
        
        start_time = time.perf_counter()
        recovered_d = attacker.attack(e, n)
        elapsed = time.perf_counter() - start_time
        
        # 验证结果
        print(f"\n[4] 验证攻击结果...")
        if recovered_d is not None:
            print(f"  ✓ 攻击成功!")
            print(f"  原始私钥 d: {d}")
            print(f"  恢复私钥 d: {recovered_d}")
            print(f"  匹配: {'✓' if d == recovered_d else '✗'}")
            print(f"  耗时: {elapsed*1000:.3f} ms")
            
            # 测试加密解密
            self._test_encryption(n, e, d, recovered_d)
        else:
            print(f"  ✗ 攻击失败")
            print(f"  耗时: {elapsed*1000:.3f} ms")
    
    def run_comparison(self, bits=1024):
        """
        运行三种攻击方法的对比测试
        
        Args:
            bits: RSA模数比特长度
        """
        print("="*70)
        print(f"三种攻击方法对比 - {bits}-bit RSA")
        print("="*70)
        
        # 生成适合新边界攻击的密钥（最宽松的条件）
        print(f"\n[1] 生成 {bits}-bit 弱RSA密钥...")
        n, e, d, p, q, boundary = self.key_gen.generate_by_boundary(bits, "new_boundary")
        
        print(f"  N 比特长度: {n.bit_length()}")
        print(f"  d 比特长度: {d.bit_length()}")
        
        # 显示理论边界对比
        print(f"\n[2] 理论边界对比...")
        boundaries = self.comparison.compare_boundaries(n)
        self._print_boundaries(boundaries)
        
        # 检查脆弱性
        print(f"\n[3] 密钥脆弱性分析...")
        vuln = self.key_gen.check_vulnerability(n, d)
        self._print_vulnerability(vuln)
        
        # 执行所有攻击
        print(f"\n[4] 执行所有攻击方法...")
        results = self.comparison.attack_all(e, n, verbose=False)
        
        # 打印详细结果
        self._print_comparison_results(results, d)
    
    def run_benchmark(self):
        """
        运行基准测试（复现论文中的实验）
        
        论文中的实验结果:
        - 1024-bit: 0.052s
        - 2048-bit: 0.152s
        - 4096-bit: 0.75s
        - 8192-bit: 4.42s
        """
        print("="*70)
        print("基准测试 - 复现论文实验结果")
        print("="*70)
        print("\n论文参考值 (Intel i5-8265U + 4GB RAM):")
        print("  1024-bit: 0.052s")
        print("  2048-bit: 0.152s")
        print("  4096-bit: 0.75s")
        print("  8192-bit: 4.42s")
        print("\n" + "="*70)
        
        results = []
        
        for config in PAPER_CONFIGS:
            bits = config['bits']
            print(f"\n测试 {bits}-bit RSA...")
            
            # 生成密钥
            n, e, d, p, q, _ = self.key_gen.generate_by_boundary(bits, "new_boundary")
            
            # 执行攻击
            start = time.perf_counter()
            recovered_d = self.new_boundary.attack(e, n)
            elapsed = time.perf_counter() - start
            
            success = recovered_d == d
            results.append({
                'bits': bits,
                'time': elapsed,
                'success': success
            })
            
            print(f"  结果: {'✓ 成功' if success else '✗ 失败'}")
            print(f"  耗时: {elapsed:.3f}s ({elapsed*1000:.2f}ms)")
        
        # 打印汇总
        print("\n" + "="*70)
        print("基准测试汇总")
        print("="*70)
        print(f"{'RSA位长':<15} {'耗时(秒)':<15} {'耗时(毫秒)':<15} {'状态':<10}")
        print("-"*70)
        for r in results:
            status = '✓' if r['success'] else '✗'
            print(f"{r['bits']:<15} {r['time']:<15.3f} {r['time']*1000:<15.2f} {status:<10}")
    
    def run_boundary_test(self, bits=1024, num_tests=5):
        """
        测试攻击边界的准确性
        
        Args:
            bits: RSA模数比特长度
            num_tests: 每个边界点的测试次数
        """
        print("="*70)
        print(f"边界测试 - {bits}-bit RSA")
        print("="*70)
        
        # 测试不同的d比例
        d_ratios = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55]
        
        print(f"\n测试不同的私钥大小 (d相对于N的比例)...")
        print(f"每个配置测试 {num_tests} 次\n")
        
        results = []
        
        for ratio in d_ratios:
            print(f"测试 d_ratio = {ratio:.2f}...")
            
            success_count = {'wiener': 0, 'bunder_tonien': 0, 'new_boundary': 0}
            
            for _ in range(num_tests):
                # 生成密钥
                n, e, d, p, q = self.key_gen.generate_weak_rsa(bits, ratio)
                
                # 测试三种攻击
                if self.wiener.attack(e, n) == d:
                    success_count['wiener'] += 1
                if self.bunder_tonien.attack(e, n) == d:
                    success_count['bunder_tonien'] += 1
                if self.new_boundary.attack(e, n) == d:
                    success_count['new_boundary'] += 1
            
            results.append({
                'ratio': ratio,
                'wiener': success_count['wiener'] / num_tests,
                'bunder_tonien': success_count['bunder_tonien'] / num_tests,
                'new_boundary': success_count['new_boundary'] / num_tests
            })
            
            print(f"  Wiener: {success_count['wiener']}/{num_tests}")
            print(f"  Bunder-Tonien: {success_count['bunder_tonien']}/{num_tests}")
            print(f"  New Boundary: {success_count['new_boundary']}/{num_tests}\n")
        
        # 打印汇总表格
        self._print_boundary_results(results)
    
    def _print_vulnerability(self, vuln):
        """打印脆弱性分析"""
        print(f"  私钥 d: {vuln['d']}")
        print(f"  d 比特长度: {vuln['d_bits']}")
        print(f"\n  Wiener攻击:")
        print(f"    边界: {vuln['wiener_bound']:.2e}")
        print(f"    脆弱: {'✓' if vuln['wiener_vulnerable'] else '✗'}")
        print(f"\n  Bunder-Tonien攻击:")
        print(f"    边界: {vuln['bunder_tonien_bound']:.2e}")
        print(f"    脆弱: {'✓' if vuln['bunder_tonien_vulnerable'] else '✗'}")
        print(f"\n  新边界攻击:")
        print(f"    边界: {vuln['new_boundary_bound']:.2e}")
        print(f"    脆弱: {'✓' if vuln['new_boundary_vulnerable'] else '✗'}")
    
    def _print_boundaries(self, boundaries):
        """打印边界对比"""
        print(f"\n  Wiener (1990): {boundaries['wiener']['formula']}")
        print(f"    边界值: {boundaries['wiener']['boundary']:.2e}")
        print(f"    比特长度: {boundaries['wiener']['boundary_bits']}")
        
        print(f"\n  Bunder-Tonien (2017): {boundaries['bunder_tonien']['formula']}")
        print(f"    边界值: {boundaries['bunder_tonien']['boundary']:.2e}")
        print(f"    比特长度: {boundaries['bunder_tonien']['boundary_bits']}")
        print(f"    相对Wiener提升: {boundaries['bunder_tonien']['improvement_ratio']:.2f}x")
        
        print(f"\n  新边界 (2023): {boundaries['new_boundary']['formula']}")
        print(f"    边界值: {boundaries['new_boundary']['boundary']:.2e}")
        print(f"    比特长度: {boundaries['new_boundary']['boundary_bits']}")
        print(f"    相对Wiener提升: {boundaries['new_boundary']['improvement_ratio']:.2f}x")
        print(f"    相对Bunder-Tonien提升: {boundaries['new_boundary']['vs_bunder_tonien']:.2f}x")
    
    def _print_comparison_results(self, results, original_d):
        """打印对比结果"""
        print(f"\n{'方法':<20} {'成功':<10} {'耗时(ms)':<15} {'匹配':<10}")
        print("-"*70)
        
        for method, result in results.items():
            success = '✓' if result['success'] else '✗'
            match = '✓' if result['success'] and result['d'] == original_d else '✗'
            time_ms = result['time'] * 1000
            print(f"{method:<20} {success:<10} {time_ms:<15.3f} {match:<10}")
    
    def _print_boundary_results(self, results):
        """打印边界测试结果"""
        print("\n" + "="*70)
        print("边界测试汇总")
        print("="*70)
        print(f"{'d比例':<10} {'Wiener':<15} {'Bunder-Tonien':<15} {'New Boundary':<15}")
        print("-"*70)
        
        for r in results:
            print(f"{r['ratio']:<10.2f} {r['wiener']*100:<14.0f}% {r['bunder_tonien']*100:<14.0f}% {r['new_boundary']*100:<14.0f}%")
    
    def _test_encryption(self, n, e, d_original, d_recovered):
        """测试加密解密"""
        print(f"\n[5] 加密解密测试...")
        
        # 测试消息
        message = 123456789
        print(f"  原始消息: {message}")
        
        # 加密
        ciphertext = pow(message, e, n)
        print(f"  密文: {ciphertext}")
        
        # 用原始私钥解密
        decrypted_original = pow(ciphertext, d_original, n)
        print(f"  原始私钥解密: {decrypted_original}")
        
        # 用恢复的私钥解密
        decrypted_recovered = pow(ciphertext, d_recovered, n)
        print(f"  恢复私钥解密: {decrypted_recovered}")
        
        # 验证
        print(f"  解密成功: {'✓' if decrypted_recovered == message else '✗'}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Wiener Attack and Improvements Demonstration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行单次新边界攻击演示
  python main.py --mode single --bits 1024 --attack new_boundary
  
  # 运行三种方法对比
  python main.py --mode compare --bits 1024
  
  # 运行基准测试（复现论文结果）
  python main.py --mode benchmark
  
  # 运行边界测试
  python main.py --mode boundary --bits 1024 --tests 5
        """
    )
    
    parser.add_argument('--mode', choices=['single', 'compare', 'benchmark', 'boundary'],
                        default='compare', help='运行模式')
    parser.add_argument('--bits', type=int, default=1024, help='RSA模数比特长度')
    parser.add_argument('--attack', choices=['wiener', 'bunder_tonien', 'new_boundary'],
                        default='new_boundary', help='攻击类型（仅用于single模式）')
    parser.add_argument('--tests', type=int, default=5, help='边界测试次数')
    
    args = parser.parse_args()
    
    demo = WienerAttackDemo()
    
    if args.mode == 'single':
        demo.run_single_attack(args.bits, args.attack)
    elif args.mode == 'compare':
        demo.run_comparison(args.bits)
    elif args.mode == 'benchmark':
        demo.run_benchmark()
    elif args.mode == 'boundary':
        demo.run_boundary_test(args.bits, args.tests)


if __name__ == "__main__":
    main()

