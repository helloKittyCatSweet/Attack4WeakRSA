#!/usr/bin/env python3
"""
Common Modulus Attack on RSA and ECC-RSA
同模数攻击实现

攻击原理:
当同一消息M使用相同模数N但不同公钥指数e1, e2加密时，
如果gcd(e1, e2) = 1，攻击者可以恢复明文M而无需知道私钥。

数学基础:
1. C1 = M^e1 mod N
2. C2 = M^e2 mod N
3. 使用扩展欧几里得算法求解: e1*x + e2*y = 1
4. 计算: M = C1^x * C2^y mod N
"""

from extended_gcd import extended_gcd
import time


class CommonModulusAttack:
    """普通RSA的同模数攻击"""
    
    def __init__(self):
        self.name = "Common Modulus Attack (RSA)"
    
    def attack(self, N, e1, e2, C1, C2, verbose=False):
        """
        执行同模数攻击
        
        Args:
            N: RSA模数
            e1: 第一个公钥指数
            e2: 第二个公钥指数
            C1: 使用e1加密的密文
            C2: 使用e2加密的密文
            verbose: 是否显示详细过程
        
        Returns:
            M: 恢复的明文，如果攻击失败则返回None
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"同模数攻击 - 普通RSA")
            print(f"{'='*70}")
            print(f"\n[1] 参数:")
            print(f"  N  = {N}")
            print(f"  e1 = {e1}")
            print(f"  e2 = {e2}")
            print(f"  C1 = {C1}")
            print(f"  C2 = {C2}")
        
        # 步骤1: 检查gcd(e1, e2) = 1
        if verbose:
            print(f"\n[2] 检查条件: gcd(e1, e2) = 1")
        
        gcd, x, y = extended_gcd(e1, e2)
        
        if verbose:
            print(f"  gcd({e1}, {e2}) = {gcd}")
        
        if gcd != 1:
            if verbose:
                print(f"  ✗ 攻击失败: e1 和 e2 不互素")
            return None
        
        if verbose:
            print(f"  ✓ e1 和 e2 互素，可以攻击")
            print(f"\n[3] 扩展欧几里得算法结果:")
            print(f"  {e1} × {x} + {e2} × {y} = {gcd}")
            print(f"  x = {x}")
            print(f"  y = {y}")
        
        # 步骤2: 计算 M = C1^x * C2^y mod N
        if verbose:
            print(f"\n[4] 计算明文:")
            print(f"  M = C1^x × C2^y mod N")
        
        start = time.perf_counter()
        
        # 处理负指数
        if x < 0:
            C1_inv = self._mod_inverse(C1, N)
            if C1_inv is None:
                if verbose:
                    print(f"  ✗ 无法计算C1的模逆元")
                return None
            C1_part = pow(C1_inv, -x, N)
        else:
            C1_part = pow(C1, x, N)
        
        if y < 0:
            C2_inv = self._mod_inverse(C2, N)
            if C2_inv is None:
                if verbose:
                    print(f"  ✗ 无法计算C2的模逆元")
                return None
            C2_part = pow(C2_inv, -y, N)
        else:
            C2_part = pow(C2, y, N)
        
        M = (C1_part * C2_part) % N
        
        elapsed = time.perf_counter() - start
        
        if verbose:
            print(f"  C1^{x} mod N = {C1_part}")
            print(f"  C2^{y} mod N = {C2_part}")
            print(f"  M = {M}")
            print(f"  耗时: {elapsed*1000:.3f} ms")
        
        return M
    
    def _mod_inverse(self, a, m):
        """计算模逆元"""
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            return None
        return x % m
    
    def verify(self, M, N, e1, e2, C1, C2, verbose=False):
        """
        验证攻击结果
        
        Args:
            M: 恢复的明文
            N: RSA模数
            e1, e2: 公钥指数
            C1, C2: 密文
            verbose: 是否显示详细信息
        
        Returns:
            bool: 验证是否通过
        """
        if verbose:
            print(f"\n[5] 验证结果:")
        
        # 重新加密验证
        C1_check = pow(M, e1, N)
        C2_check = pow(M, e2, N)
        
        match1 = C1_check == C1
        match2 = C2_check == C2
        
        if verbose:
            print(f"  M^e1 mod N = {C1_check}")
            print(f"  C1        = {C1}")
            print(f"  匹配: {'✓' if match1 else '✗'}")
            print(f"\n  M^e2 mod N = {C2_check}")
            print(f"  C2        = {C2}")
            print(f"  匹配: {'✓' if match2 else '✗'}")
        
        return match1 and match2


class ECCRSACommonModulusAttack:
    """ECC-RSA变体的同模数攻击"""
    
    def __init__(self, a, b, p):
        """
        初始化椭圆曲线参数
        
        Args:
            a, b: 椭圆曲线参数 y^2 = x^3 + ax + b
            p: 素数模数
        """
        self.name = "Common Modulus Attack (ECC-RSA)"
        self.a = a
        self.b = b
        self.p = p
    
    def point_add(self, P, Q):
        """椭圆曲线点加法"""
        if P is None:
            return Q
        if Q is None:
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        if x1 == x2:
            if y1 == y2:
                # 点倍乘
                s = (3 * x1 * x1 + self.a) * pow(2 * y1, -1, self.p) % self.p
            else:
                # P + (-P) = O
                return None
        else:
            # 普通点加
            s = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p
        
        x3 = (s * s - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def scalar_mult(self, k, P):
        """椭圆曲线标量乘法"""
        if k == 0:
            return None
        if k < 0:
            # 负数乘法: -k*P = k*(-P)
            k = -k
            P = (P[0], -P[1] % self.p)
        
        result = None
        addend = P
        
        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1
        
        return result
    
    def attack(self, N, e1, e2, C1, C2, verbose=False):
        """
        对ECC-RSA变体执行同模数攻击
        
        Args:
            N: 模数
            e1, e2: 公钥指数
            C1, C2: 密文点 (r, y)
            verbose: 是否显示详细过程
        
        Returns:
            M: 恢复的明文点
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"同模数攻击 - ECC-RSA变体")
            print(f"{'='*70}")
            print(f"\n[1] 椭圆曲线参数:")
            print(f"  y² = x³ + {self.a}x + {self.b} (mod {self.p})")
            print(f"\n[2] 攻击参数:")
            print(f"  N  = {N}")
            print(f"  e1 = {e1}")
            print(f"  e2 = {e2}")
            print(f"  C1 = {C1}")
            print(f"  C2 = {C2}")
        
        # 检查gcd(e1, e2) = 1
        gcd, x, y = extended_gcd(e1, e2)
        
        if verbose:
            print(f"\n[3] 扩展欧几里得算法:")
            print(f"  gcd({e1}, {e2}) = {gcd}")
            print(f"  {e1} × {x} + {e2} × {y} = {gcd}")
        
        if gcd != 1:
            if verbose:
                print(f"  ✗ 攻击失败: e1 和 e2 不互素")
            return None
        
        if verbose:
            print(f"  ✓ 可以攻击")
            print(f"\n[4] 计算明文点:")
            print(f"  M = x·C1 + y·C2")
            print(f"  M = {x}·C1 + {y}·C2")
        
        start = time.perf_counter()
        
        # 计算 M = x*C1 + y*C2
        P1 = self.scalar_mult(x, C1)
        P2 = self.scalar_mult(y, C2)
        M = self.point_add(P1, P2)
        
        elapsed = time.perf_counter() - start
        
        if verbose:
            print(f"  {x}·C1 = {P1}")
            print(f"  {y}·C2 = {P2}")
            print(f"  M = {M}")
            print(f"  耗时: {elapsed*1000:.3f} ms")
        
        return M


if __name__ == "__main__":
    # 简单测试
    print("Common Modulus Attack - 基本测试")
    
    # 测试普通RSA
    attacker = CommonModulusAttack()
    
    N = 3233
    e1 = 3
    e2 = 5
    M = 42
    
    C1 = pow(M, e1, N)
    C2 = pow(M, e2, N)
    
    recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=True)
    
    if recovered_M == M:
        print(f"\n✓ 攻击成功! 恢复的明文: {recovered_M}")
    else:
        print(f"\n✗ 攻击失败")

