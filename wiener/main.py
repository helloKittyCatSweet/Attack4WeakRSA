import argparse
import time
from rsa_weak_key_generator import WeakRSAGenerator
from wiener_attack import WienerAttack, BunderTonienAttack, NewBoundaryAttack, AttackComparison
from config import DEFAULT_CONFIG, BENCHMARK_CONFIGS, PAPER_CONFIGS


class WienerAttackDemo:
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
        print("=" * 70)
        print(f"维纳攻击演示 - {attack_type.upper()}")
        print("=" * 70)

        # 生成弱RSA密钥
        print(f"\n[1] 生成 {bits}-bit 弱RSA密钥...")
        n, e, d, p, q, boundary = self.key_gen.generate_by_boundary(bits, attack_type)

        print(f"  N 比特长度: {n.bit_length()}")
        print(f"  e 比特长度: {e.bit_length()}")
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
            print(f"  耗时: {elapsed * 1000:.3f} ms")

            # 测试加密解密
            self._test_encryption(n, e, d, recovered_d)
        else:
            print(f"  ✗ 攻击失败")
            print(f"  可能原因: 连分数收敛项未找到正确私钥")
            print(f"  耗时: {elapsed * 1000:.3f} ms")

    def run_comparison(self, bits=1024):
        """
        运行三种攻击方法的对比测试

        Args:
            bits: RSA模数比特长度
        """
        print("=" * 70)
        print(f"三种攻击方法对比 - {bits}-bit RSA")
        print("=" * 70)

        # 为每种攻击生成合适的密钥
        results_all = {}

        for attack_type in ["wiener", "bunder_tonien", "new_boundary"]:
            print(f"\n[1] 为 {attack_type} 攻击生成 {bits}-bit 弱RSA密钥...")
            n, e, d, p, q, boundary = self.key_gen.generate_by_boundary(bits, attack_type)

            print(f"  N 比特长度: {n.bit_length()}")
            print(f"  d 比特长度: {d.bit_length()}")
            print(f"  理论边界: {boundary:.2e}")
            print(f"  d < 边界: {'✓' if d < boundary else '✗'}")

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
            self._print_comparison_results(results, d, attack_type)

            results_all[attack_type] = {
                'n': n, 'e': e, 'd': d, 'results': results
            }

        return results_all

    def run_targeted_comparison(self, bits=1024):
        """
        针对同一密钥运行三种攻击方法对比
        """
        print("=" * 70)
        print(f"针对性对比测试 - {bits}-bit RSA")
        print("=" * 70)

        # 生成一个中等大小的私钥，让部分攻击能成功
        print(f"\n[1] 生成 {bits}-bit RSA密钥 (中等大小私钥)...")

        # 尝试生成一个在Bunder-Tonien边界内但在Wiener边界外的密钥
        max_attempts = 10
        for attempt in range(max_attempts):
            n, e, d, p, q = self.key_gen.generate_weak_rsa(bits, d_ratio=0.4)
            wiener_bound = self.wiener.get_boundary(n)
            bt_bound = self.bunder_tonien.get_boundary(n)
            new_bound = self.new_boundary.get_boundary(n)

            # 检查是否在合适范围内：大于Wiener边界但小于Bunder-Tonien边界
            if d > wiener_bound and d < bt_bound:
                print(f"  找到合适密钥 (尝试 {attempt + 1} 次)")
                break
        else:
            # 如果没找到，使用第一个生成的密钥
            print("  使用生成的密钥")

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
        results = self.comparison.attack_all(e, n, verbose=True)

        return results

    def run_benchmark(self):
        """
        运行基准测试（复现论文中的实验）
        """
        print("=" * 70)
        print("基准测试 - 攻击性能测试")
        print("=" * 70)

        results = []

        for config in BENCHMARK_CONFIGS:
            bits = config['bits']
            print(f"\n测试 {bits}-bit RSA...")

            # 生成适合新边界攻击的密钥
            n, e, d, p, q, boundary = self.key_gen.generate_by_boundary(bits, "new_boundary")

            print(f"  N 比特长度: {n.bit_length()}")
            print(f"  d 比特长度: {d.bit_length()}")

            # 执行攻击
            start = time.perf_counter()
            recovered_d = self.new_boundary.attack(e, n)
            elapsed = time.perf_counter() - start

            success = recovered_d == d
            results.append({
                'bits': bits,
                'time': elapsed,
                'success': success,
                'n_bits': n.bit_length(),
                'd_bits': d.bit_length()
            })

            status = '✓ 成功' if success else '✗ 失败'
            print(f"  结果: {status}")
            print(f"  耗时: {elapsed:.3f}s ({elapsed * 1000:.2f}ms)")

        # 打印汇总
        print("\n" + "=" * 70)
        print("基准测试汇总")
        print("=" * 70)
        print(f"{'RSA位长':<10} {'N比特':<10} {'d比特':<10} {'耗时(秒)':<12} {'耗时(毫秒)':<14} {'状态':<10}")
        print("-" * 70)
        for r in results:
            status = '✓' if r['success'] else '✗'
            print(
                f"{r['bits']:<10} {r['n_bits']:<10} {r['d_bits']:<10} {r['time']:<12.3f} {r['time'] * 1000:<14.2f} {status:<10}")

    def run_boundary_test(self, bits=1024, num_tests=3):
        """
        测试攻击边界的准确性
        """
        print("=" * 70)
        print(f"边界测试 - {bits}-bit RSA")
        print("=" * 70)

        # 测试不同的攻击类型
        attack_types = ['wiener', 'bunder_tonien', 'new_boundary']

        print(f"\n测试不同攻击方法的有效性...")
        print(f"每个攻击类型测试 {num_tests} 次\n")

        results = []

        for attack_type in attack_types:
            print(f"测试 {attack_type} 攻击...")

            success_count = 0
            total_time = 0

            for i in range(num_tests):
                print(f"  第 {i + 1} 次测试...")

                # 生成对应攻击的弱密钥
                n, e, d, p, q, boundary = self.key_gen.generate_by_boundary(bits, attack_type)

                # 选择攻击器
                if attack_type == "wiener":
                    attacker = self.wiener
                elif attack_type == "bunder_tonien":
                    attacker = self.bunder_tonien
                else:
                    attacker = self.new_boundary

                # 执行攻击
                start_time = time.perf_counter()
                recovered_d = attacker.attack(e, n)
                elapsed = time.perf_counter() - start_time
                total_time += elapsed

                if recovered_d == d:
                    success_count += 1
                    print(f"    ✓ 成功 - 耗时: {elapsed * 1000:.2f}ms")
                else:
                    print(f"    ✗ 失败 - 耗时: {elapsed * 1000:.2f}ms")

            avg_time = total_time / num_tests
            success_rate = success_count / num_tests

            results.append({
                'attack_type': attack_type,
                'success_rate': success_rate,
                'avg_time': avg_time,
                'success_count': success_count,
                'total_tests': num_tests
            })

            print(f"  成功率: {success_count}/{num_tests} ({success_rate * 100:.1f}%)")
            print(f"  平均耗时: {avg_time * 1000:.2f}ms\n")

        # 打印汇总表格
        self._print_boundary_results(results)

    def _print_vulnerability(self, vuln):
        """打印脆弱性分析"""
        print(f"  私钥 d 比特长度: {vuln['d_bits']}")
        print(f"\n  Wiener攻击:")
        print(f"    边界: {vuln['wiener_bound']:.2e}")
        print(f"    边界比特: {vuln['wiener_bound_bits']}")
        print(f"    脆弱: {'✓' if vuln['wiener_vulnerable'] else '✗'}")

        print(f"\n  Bunder-Tonien攻击:")
        print(f"    边界: {vuln['bunder_tonien_bound']:.2e}")
        print(f"    边界比特: {vuln['bunder_tonien_bound_bits']}")
        print(f"    脆弱: {'✓' if vuln['bunder_tonien_vulnerable'] else '✗'}")

        print(f"\n  新边界攻击:")
        print(f"    边界: {vuln['new_boundary_bound']:.2e}")
        print(f"    边界比特: {vuln['new_boundary_bound_bits']}")
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

    def _print_comparison_results(self, results, original_d, key_type):
        """打印对比结果"""
        print(f"\n[{key_type.upper()}密钥] 攻击结果:")
        print(f"{'方法':<20} {'成功':<8} {'耗时(ms)':<12} {'匹配':<8} {'d恢复':<15}")
        print("-" * 70)

        for method, result in results.items():
            success = '✓' if result['success'] else '✗'
            match = '✓' if result['success'] and result['d'] == original_d else '✗'
            time_ms = result['time'] * 1000

            d_recovered = "是" if result['success'] else "否"
            if result['success']:
                d_recovered += f"({result['d'].bit_length()}位)"
            else:
                d_recovered += "(无)"

            print(f"{method:<20} {success:<8} {time_ms:<12.3f} {match:<8} {d_recovered:<15}")

    def _print_boundary_results(self, results):
        """打印边界测试结果"""
        print("\n" + "=" * 70)
        print("边界测试汇总")
        print("=" * 70)
        print(f"{'攻击类型':<15} {'成功率':<10} {'平均耗时(ms)':<15} {'成功数':<10}")
        print("-" * 70)

        for r in results:
            success_rate = f"{r['success_rate'] * 100:.1f}%"
            avg_time = f"{r['avg_time'] * 1000:.2f}"
            success_count = f"{r['success_count']}/{r['total_tests']}"

            print(f"{r['attack_type']:<15} {success_rate:<10} {avg_time:<15} {success_count:<10}")

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
        success = decrypted_recovered == message
        print(f"  解密成功: {'✓' if success else '✗'}")
        return success


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Wiener Attack and Improvements Demonstration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行单次新边界攻击演示
  python main.py --mode single --bits 1024 --attack new_boundary

  # 运行三种方法对比（针对性测试）
  python main.py --mode compare --bits 1024

  # 运行基准测试
  python main.py --mode benchmark

  # 运行边界测试
  python main.py --mode boundary --bits 1024 --tests 3
        """
    )

    parser.add_argument('--mode', choices=['single', 'compare', 'targeted', 'benchmark', 'boundary'],
                        default='targeted', help='运行模式')
    parser.add_argument('--bits', type=int, default=1024, help='RSA模数比特长度')
    parser.add_argument('--attack', choices=['wiener', 'bunder_tonien', 'new_boundary'],
                        default='new_boundary', help='攻击类型（仅用于single模式）')
    parser.add_argument('--tests', type=int, default=3, help='边界测试次数')

    args = parser.parse_args()

    demo = WienerAttackDemo()

    if args.mode == 'single':
        demo.run_single_attack(args.bits, args.attack)
    elif args.mode == 'compare':
        demo.run_comparison(args.bits)
    elif args.mode == 'targeted':
        demo.run_targeted_comparison(args.bits)
    elif args.mode == 'benchmark':
        demo.run_benchmark()
    elif args.mode == 'boundary':
        demo.run_boundary_test(args.bits, args.tests)


if __name__ == "__main__":
    main()