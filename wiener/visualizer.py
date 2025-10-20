"""
Visualization tools for Wiener attack analysis
维纳攻击分析可视化工具
"""

import math


class AttackVisualizer:
    """攻击结果可视化"""
    
    @staticmethod
    def print_header(title):
        """打印标题"""
        width = 70
        print("\n" + "="*width)
        print(title.center(width))
        print("="*width)
    
    @staticmethod
    def print_section(title):
        """打印章节标题"""
        print(f"\n[{title}]")
        print("-"*70)
    
    @staticmethod
    def print_key_info(n, e, d, p, q):
        """打印密钥信息"""
        print(f"  N = {n}")
        print(f"  e = {e}")
        print(f"  d = {d}")
        print(f"  p = {p}")
        print(f"  q = {q}")
        print(f"\n  比特长度:")
        print(f"    N: {n.bit_length()} bits")
        print(f"    e: {e.bit_length()} bits")
        print(f"    d: {d.bit_length()} bits")
        print(f"    p: {p.bit_length()} bits")
        print(f"    q: {q.bit_length()} bits")
    
    @staticmethod
    def print_boundary_comparison(n, d):
        """打印边界对比"""
        wiener_bound = n ** 0.25 / 3
        bt_bound = 2 * math.sqrt(2 * n)
        new_bound = math.sqrt(8.24264 * n)
        
        print(f"\n  私钥 d = {d}")
        print(f"  d 比特长度: {d.bit_length()}")
        print(f"\n  {'攻击方法':<20} {'边界值':<20} {'d < 边界':<10} {'比特长度':<10}")
        print("  " + "-"*65)
        
        print(f"  {'Wiener (1990)':<20} {wiener_bound:<20.2e} {str(d < wiener_bound):<10} {int(math.log2(wiener_bound)) if wiener_bound > 0 else 0:<10}")
        print(f"  {'Bunder-Tonien':<20} {bt_bound:<20.2e} {str(d < bt_bound):<10} {int(math.log2(bt_bound)) if bt_bound > 0 else 0:<10}")
        print(f"  {'New Boundary':<20} {new_bound:<20.2e} {str(d < new_bound):<10} {int(math.log2(new_bound)) if new_bound > 0 else 0:<10}")
    
    @staticmethod
    def print_attack_result(method, success, d_original, d_recovered, time_ms):
        """打印攻击结果"""
        print(f"\n  攻击方法: {method}")
        print(f"  结果: {'✓ 成功' if success else '✗ 失败'}")
        if success:
            print(f"  原始私钥: {d_original}")
            print(f"  恢复私钥: {d_recovered}")
            print(f"  匹配: {'✓' if d_original == d_recovered else '✗'}")
        print(f"  耗时: {time_ms:.3f} ms")
    
    @staticmethod
    def print_comparison_table(results):
        """打印对比表格"""
        print(f"\n  {'方法':<20} {'成功':<10} {'耗时(ms)':<15} {'耗时(s)':<15}")
        print("  " + "-"*65)
        
        for method, result in results.items():
            success = '✓' if result['success'] else '✗'
            time_ms = result['time'] * 1000
            time_s = result['time']
            print(f"  {method:<20} {success:<10} {time_ms:<15.3f} {time_s:<15.6f}")
    
    @staticmethod
    def print_benchmark_table(results):
        """打印基准测试表格"""
        print(f"\n  {'RSA位长':<15} {'耗时(秒)':<15} {'耗时(毫秒)':<15} {'状态':<10}")
        print("  " + "-"*60)
        
        for r in results:
            status = '✓' if r['success'] else '✗'
            print(f"  {r['bits']:<15} {r['time']:<15.3f} {r['time']*1000:<15.2f} {status:<10}")
    
    @staticmethod
    def print_boundary_test_table(results):
        """打印边界测试表格"""
        print(f"\n  {'d比例':<10} {'Wiener':<15} {'Bunder-Tonien':<20} {'New Boundary':<15}")
        print("  " + "-"*65)
        
        for r in results:
            print(f"  {r['ratio']:<10.2f} {r['wiener']*100:<14.0f}% {r['bunder_tonien']*100:<19.0f}% {r['new_boundary']*100:<14.0f}%")
    
    @staticmethod
    def print_ascii_chart(data, title="Chart", max_width=50):
        """打印ASCII图表"""
        print(f"\n  {title}")
        print("  " + "-"*max_width)
        
        if not data:
            return
        
        max_val = max(data.values())
        
        for label, value in data.items():
            bar_length = int((value / max_val) * max_width) if max_val > 0 else 0
            bar = "█" * bar_length
            print(f"  {label:<15} {bar} {value:.2e}")
    
    @staticmethod
    def print_theoretical_analysis():
        """打印理论分析"""
        AttackVisualizer.print_header("理论分析")
        
        print("\n1. Wiener攻击 (1990)")
        print("   条件: d < N^0.25 / 3")
        print("   原理: 利用连分数展开 e/N ≈ k/d")
        print("   复杂度: O(log N)")
        
        print("\n2. Bunder-Tonien攻击 (2017)")
        print("   条件: d < 2√(2N)")
        print("   改进: 放宽了Wiener的边界条件")
        print("   提升: 约 N^0.25 倍")
        
        print("\n3. 新边界攻击 (2023)")
        print("   条件: d < √(8.24264N)")
        print("   推导: 通过导数和极限分析")
        print("   公式: α = 8 + 6√2 ≈ 16.4853")
        print("         d < (α/2)√N")
        print("   提升: 相对Bunder-Tonien约1.01倍")
        
        print("\n关键不等式 (Lemma 3.1):")
        print("   (3√2 - 2N + 4) / (2N - 3√(2N)) < 1/(αN)")
        print("   当 N → ∞ 时，左边 → 1/(8 + 6√2)")
    
    @staticmethod
    def print_security_recommendations():
        """打印安全建议"""
        AttackVisualizer.print_header("安全建议")
        
        print("\n✓ 推荐做法:")
        print("  1. 使用标准RSA密钥生成算法")
        print("  2. 确保 d > N^0.5")
        print("  3. RSA模数 ≥ 2048位")
        print("  4. 公钥指数 e = 65537")
        print("  5. 遵循NIST SP 800-56B标准")
        
        print("\n✗ 避免做法:")
        print("  1. 不要人为选择小的私钥d")
        print("  2. 不要使用过小的RSA模数")
        print("  3. 不要为了计算效率而牺牲安全性")
        print("  4. 不要重用密钥对")
        
        print("\n⚠ 脆弱性检测:")
        print("  如果 d < √(8.24264N)，密钥可能被新边界攻击破解")
        print("  如果 d < 2√(2N)，密钥可能被Bunder-Tonien攻击破解")
        print("  如果 d < N^0.25/3，密钥可能被Wiener攻击破解")
    
    @staticmethod
    def print_complexity_analysis():
        """打印复杂度分析"""
        AttackVisualizer.print_header("复杂度分析")
        
        print("\n时间复杂度: O(log N)")
        print("\n主要步骤:")
        print("  1. 连分数展开 (欧几里得算法): O(log N)")
        print("  2. 收敛项计算: O(log N)")
        print("  3. 候选验证: O(log N) 次，每次 O(1)")
        print("\n空间复杂度: O(log N)")
        print("  存储连分数收敛项")
        
        print("\n实际性能:")
        print("  512-bit RSA:  ~0.02s")
        print("  1024-bit RSA: ~0.05s")
        print("  2048-bit RSA: ~0.15s")
        print("  4096-bit RSA: ~0.75s")
        print("  8192-bit RSA: ~4.5s")
        
        print("\n与暴力破解对比:")
        print("  暴力破解: O(2^(d的比特长度))")
        print("  Wiener攻击: O(log N)")
        print("  效率提升: 指数级")


class ProgressBar:
    """进度条"""
    
    def __init__(self, total, width=50, prefix="Progress"):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.current = 0
    
    def update(self, current):
        """更新进度"""
        self.current = current
        percent = (current / self.total) * 100
        filled = int((current / self.total) * self.width)
        bar = "█" * filled + "-" * (self.width - filled)
        print(f"\r  {self.prefix}: |{bar}| {percent:.1f}% ({current}/{self.total})", end="", flush=True)
    
    def finish(self):
        """完成"""
        self.update(self.total)
        print()


class ColorPrinter:
    """彩色打印（如果终端支持）"""
    
    # ANSI颜色代码
    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m',
        'bold': '\033[1m'
    }
    
    @classmethod
    def print_colored(cls, text, color='white', bold=False):
        """打印彩色文本"""
        color_code = cls.COLORS.get(color, cls.COLORS['white'])
        bold_code = cls.COLORS['bold'] if bold else ''
        reset_code = cls.COLORS['reset']
        print(f"{bold_code}{color_code}{text}{reset_code}")
    
    @classmethod
    def print_success(cls, text):
        """打印成功消息"""
        cls.print_colored(f"✓ {text}", 'green', bold=True)
    
    @classmethod
    def print_error(cls, text):
        """打印错误消息"""
        cls.print_colored(f"✗ {text}", 'red', bold=True)
    
    @classmethod
    def print_warning(cls, text):
        """打印警告消息"""
        cls.print_colored(f"⚠ {text}", 'yellow', bold=True)
    
    @classmethod
    def print_info(cls, text):
        """打印信息消息"""
        cls.print_colored(f"ℹ {text}", 'cyan')

