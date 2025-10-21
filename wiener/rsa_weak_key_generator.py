"""
RSA Weak Key Generator for Wiener Attack Testing
生成具有小私钥的弱RSA密钥对
"""

import random
import math
from Crypto.Util.number import getPrime, inverse, GCD

from wiener_attack import WienerAttack, BunderTonienAttack, NewBoundaryAttack


class WeakRSAGenerator:
    """生成易受Wiener攻击的弱RSA密钥"""
    
    def __init__(self):
        pass

    def _isqrt(self, n):
        """整数平方根"""
        if n < 0:
            return 0
        if n == 0:
            return 0

        # 使用牛顿法
        x = n
        y = (x + 1) // 2

        while y < x:
            x = y
            y = (x + n // x) // 2

        return x
    
    def generate_weak_rsa(self, bits=1024, d_ratio=0.25):
        """
        生成具有小私钥的RSA密钥对
        
        Args:
            bits: RSA模数的比特长度
            d_ratio: d相对于N的比例，用于控制d的大小
                    - Wiener攻击: d < N^0.25 / 3
                    - Bunder-Tonien: d < 2*sqrt(2*N)
                    - New boundary: d < sqrt(8.24264*N)
        
        Returns:
            (n, e, d, p, q): RSA参数
        """
        # 生成两个大素数
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)
        
        while p == q:
            q = getPrime(bits // 2)
        
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # 根据比例计算目标d的大小
        target_d_bits = int(bits * d_ratio)
        
        # 生成小的d
        d = self._generate_small_d(phi, target_d_bits)
        
        # 计算对应的e
        try:
            e = inverse(d, phi)
        except:
            # 如果d和phi不互质，重新生成
            return self.generate_weak_rsa(bits, d_ratio)
        
        return n, e, d, p, q
    
    def _generate_small_d(self, phi, target_bits):
        """生成指定比特长度的小私钥d"""
        max_attempts = 1000
        
        for _ in range(max_attempts):
            # 生成目标比特长度的随机数
            d = random.randrange(2**(target_bits - 1), 2**target_bits)
            
            # 确保d与phi互质
            if GCD(d, phi) == 1:
                return d
        
        # 如果失败，使用简单方法
        d = 3
        while GCD(d, phi) != 1:
            d += 2
        return d
    
    def generate_by_boundary(self, bits=1024, attack_type="wiener"):
        """
        根据攻击类型生成对应边界的弱RSA密钥

        Args:
            bits: RSA模数比特长度
            attack_type: "wiener", "bunder_tonien", 或 "new_boundary"

        Returns:
            (n, e, d, p, q, boundary): RSA参数和理论边界值
        """
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)

        while p == q:
            q = getPrime(bits // 2)

        n = p * q
        phi = (p - 1) * (q - 1)

        # 根据攻击类型计算边界
        if attack_type == "wiener":
            # d < N^0.25 / 3
            boundary = int(pow(n, 0.25) / 3)
        elif attack_type == "bunder_tonien":
            # d < 2*sqrt(2*N)
            # 使用整数平方根避免浮点溢出
            boundary = 2 * self._isqrt(2 * n)
        elif attack_type == "new_boundary":
            # d < sqrt(8.24264*N)
            # 使用整数平方根避免浮点溢出
            # 8.24264 ≈ 824264/100000
            boundary = self._isqrt(824264 * n // 100000)
        else:
            raise ValueError(f"Unknown attack type: {attack_type}")

        # 生成小于边界的d
        d = self._generate_d_below_boundary(phi, boundary)

        # 计算e
        try:
            e = inverse(d, phi)
        except:
            return self.generate_by_boundary(bits, attack_type)

        return n, e, d, p, q, boundary
    
    def _generate_d_below_boundary(self, phi, boundary):
        """生成小于指定边界的d"""
        max_attempts = 1000

        # 确保边界是整数
        if isinstance(boundary, float):
            boundary = int(boundary)

        # 确保边界不会太小
        if boundary < 100:
            boundary = 100

        for _ in range(max_attempts):
            # 在边界范围内随机选择，偏向较小的值
            # 使用对数分布使得小值更容易被选中
            upper = min(boundary, phi - 1)
            lower = max(3, upper // 10)  # 从边界的1/10开始

            if lower >= upper:
                lower = 3
                upper = max(100, min(boundary, phi - 1))

            d = random.randrange(lower, upper)

            if GCD(d, phi) == 1:
                return d

        # 备用方案：从小值开始搜索
        d = 3
        while d < boundary and GCD(d, phi) != 1:
            d += 2

        if d >= boundary:
            d = boundary - 1
            while d > 2 and GCD(d, phi) != 1:
                d -= 2

        return d

    def check_vulnerability(self, n, d):
        """
        检查RSA密钥对各种Wiener攻击的脆弱性

        Returns:
            dict: 包含各种攻击边界和脆弱性信息的字典
        """
        wiener_attack = WienerAttack()
        bunder_tonien_attack = BunderTonienAttack()
        new_boundary_attack = NewBoundaryAttack()

        wiener_bound = wiener_attack.get_boundary(n)
        bt_bound = bunder_tonien_attack.get_boundary(n)
        new_bound = new_boundary_attack.get_boundary(n)

        return {
            'd': d,
            'd_bits': d.bit_length(),
            'wiener_bound': wiener_bound,
            'wiener_bound_bits': wiener_bound.bit_length() if wiener_bound > 0 else 0,
            'wiener_vulnerable': d < wiener_bound,
            'bunder_tonien_bound': bt_bound,
            'bunder_tonien_bound_bits': bt_bound.bit_length() if bt_bound > 0 else 0,
            'bunder_tonien_vulnerable': d < bt_bound,
            'new_boundary_bound': new_bound,
            'new_boundary_bound_bits': new_bound.bit_length() if new_bound > 0 else 0,
            'new_boundary_vulnerable': d < new_bound
        }

