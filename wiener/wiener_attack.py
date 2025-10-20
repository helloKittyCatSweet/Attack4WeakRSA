"""
Wiener Attack and its improvements implementation
维纳攻击及其改进版本的实现
"""

import math
import time
from continued_fraction import ContinuedFraction


class WienerAttack:
    """原始Wiener攻击 (1990)"""
    
    def __init__(self):
        self.cf = ContinuedFraction()
    
    def attack(self, e, n):
        """
        执行Wiener攻击
        
        条件: d < N^0.25 / 3
        
        Args:
            e: 公钥指数
            n: RSA模数
            
        Returns:
            d: 私钥 (如果成功), None (如果失败)
        """
        # 计算e/n的连分数收敛项
        convergents = self.cf.compute_convergents(e, n)
        
        for k, d in convergents:
            # 跳过无效值
            if k == 0 or d == 0:
                continue
            
            # 检查是否满足 ed ≡ 1 (mod φ(n))
            if self._check_candidate(e, n, k, d):
                return d
        
        return None
    
    def _check_candidate(self, e, n, k, d):
        """
        检查候选私钥d是否正确
        
        通过以下方式验证:
        1. ed - 1 应该能被 k 整除
        2. 计算 φ(n) = (ed - 1) / k
        3. 从 φ(n) 和 n 恢复 p 和 q
        4. 验证 pq = n
        """
        # 检查 ed ≡ 1 (mod k)
        if (e * d - 1) % k != 0:
            return False
        
        phi = (e * d - 1) // k
        
        # 从 n 和 φ(n) 计算 p 和 q
        # n = pq, φ(n) = (p-1)(q-1) = n - (p+q) + 1
        # 因此: p + q = n - φ(n) + 1
        s = n - phi + 1
        
        # 解方程: x^2 - sx + n = 0
        # p, q = (s ± sqrt(s^2 - 4n)) / 2
        discriminant = s * s - 4 * n
        
        if discriminant < 0:
            return False
        
        sqrt_d = self._isqrt(discriminant)
        
        # 检查是否为完全平方数
        if sqrt_d * sqrt_d != discriminant:
            return False
        
        p = (s + sqrt_d) // 2
        q = (s - sqrt_d) // 2
        
        # 验证
        return p * q == n and p > 1 and q > 1
    
    def _isqrt(self, n):
        """整数平方根"""
        if n < 0:
            return -1
        if n == 0:
            return 0
        
        x = n
        y = (x + 1) // 2
        
        while y < x:
            x = y
            y = (x + n // x) // 2
        
        return x
    
    def get_boundary(self, n):
        """返回Wiener攻击的理论边界"""
        return pow(n, 0.25) / 3


class BunderTonienAttack(WienerAttack):
    """Bunder-Tonien改进攻击 (2017)"""

    def attack(self, e, n):
        """
        执行Bunder-Tonien攻击

        条件: d < 2*sqrt(2*N)

        使用与Wiener相同的连分数方法，但边界更宽松
        """
        # 基本方法与Wiener相同
        return super().attack(e, n)

    def get_boundary(self, n):
        """返回Bunder-Tonien攻击的理论边界"""
        # 使用整数平方根避免浮点溢出
        return 2 * self._isqrt(2 * n)


class NewBoundaryAttack(WienerAttack):
    """
    新边界攻击 (2023)
    基于论文: "A New Boundary of Minimum Private Key on Wiener Attack Against RSA Algorithm"
    """
    
    def attack(self, e, n):
        """
        执行新边界攻击
        
        条件: d < sqrt(8.24264*N) ≈ sqrt((8 + 6*sqrt(2))*N)
        
        通过改进的不等式分析，扩大了可攻击的私钥范围
        """
        # 基本方法与Wiener相同，但理论边界更高
        return super().attack(e, n)
    
    def get_boundary(self, n):
        """
        返回新边界攻击的理论边界

        根据论文 Lemma 3.1:
        α = 8 + 6*sqrt(2) ≈ 16.4853
        d < (α/2) * sqrt(N) ≈ sqrt(8.24264*N)
        """
        # 使用整数平方根避免浮点溢出
        # 8.24264 ≈ 824264/100000
        return self._isqrt(824264 * n // 100000)
    
    def verify_inequality(self, n):
        """
        验证论文中的不等式 (Lemma 3.1)

        (3*sqrt(2) - 2*N + 4) / (2*N - 3*sqrt(2*N)) < 1 / (α*N)

        当 N → ∞ 时，左边趋向于 1/(8 + 6*sqrt(2))
        """
        # 对于大整数，使用近似计算
        sqrt_2 = 1.41421356237
        sqrt_2n = self._isqrt(2 * n)

        numerator = 3 * sqrt_2 - 2 * n + 4
        denominator = 2 * n - 3 * sqrt_2n

        if denominator <= 0:
            return False

        left_side = numerator / denominator

        alpha = 8 + 6 * sqrt_2
        right_side = 1 / (alpha * n)

        return left_side < right_side


class AttackComparison:
    """攻击方法对比工具"""
    
    def __init__(self):
        self.wiener = WienerAttack()
        self.bunder_tonien = BunderTonienAttack()
        self.new_boundary = NewBoundaryAttack()
    
    def compare_boundaries(self, n):
        """
        比较三种攻击方法的理论边界
        
        Returns:
            dict: 包含各种边界值的字典
        """
        wiener_bound = self.wiener.get_boundary(n)
        bt_bound = self.bunder_tonien.get_boundary(n)
        new_bound = self.new_boundary.get_boundary(n)
        
        return {
            "n": n,
            "n_bits": n.bit_length(),
            "wiener": {
                "boundary": wiener_bound,
                "boundary_bits": int(math.log2(wiener_bound)) if wiener_bound > 0 else 0,
                "formula": "N^0.25 / 3"
            },
            "bunder_tonien": {
                "boundary": bt_bound,
                "boundary_bits": int(math.log2(bt_bound)) if bt_bound > 0 else 0,
                "formula": "2*sqrt(2*N)",
                "improvement_ratio": bt_bound / wiener_bound if wiener_bound > 0 else 0
            },
            "new_boundary": {
                "boundary": new_bound,
                "boundary_bits": int(math.log2(new_bound)) if new_bound > 0 else 0,
                "formula": "sqrt(8.24264*N)",
                "improvement_ratio": new_bound / wiener_bound if wiener_bound > 0 else 0,
                "vs_bunder_tonien": new_bound / bt_bound if bt_bound > 0 else 0
            }
        }
    
    def attack_all(self, e, n, verbose=True):
        """
        使用三种方法尝试攻击
        
        Returns:
            dict: 包含各种攻击结果和时间的字典
        """
        results = {}
        
        # Wiener攻击
        start = time.perf_counter()
        d_wiener = self.wiener.attack(e, n)
        time_wiener = time.perf_counter() - start
        results["wiener"] = {
            "success": d_wiener is not None,
            "d": d_wiener,
            "time": time_wiener
        }
        
        # Bunder-Tonien攻击
        start = time.perf_counter()
        d_bt = self.bunder_tonien.attack(e, n)
        time_bt = time.perf_counter() - start
        results["bunder_tonien"] = {
            "success": d_bt is not None,
            "d": d_bt,
            "time": time_bt
        }
        
        # 新边界攻击
        start = time.perf_counter()
        d_new = self.new_boundary.attack(e, n)
        time_new = time.perf_counter() - start
        results["new_boundary"] = {
            "success": d_new is not None,
            "d": d_new,
            "time": time_new
        }
        
        if verbose:
            self._print_results(results)
        
        return results
    
    def _print_results(self, results):
        """打印攻击结果"""
        print("\n" + "="*60)
        print("攻击结果对比")
        print("="*60)
        
        for method, result in results.items():
            print(f"\n{method.upper()}:")
            print(f"  成功: {'✓' if result['success'] else '✗'}")
            if result['success']:
                print(f"  私钥 d: {result['d']}")
            print(f"  耗时: {result['time']*1000:.3f} ms")

