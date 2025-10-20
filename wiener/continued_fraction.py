"""
Continued Fraction implementation for Wiener attack
连分数算法实现
"""

class ContinuedFraction:
    """连分数展开和收敛项计算"""
    
    @staticmethod
    def compute_convergents(e, n):
        """
        计算 e/n 的连分数收敛项
        
        Args:
            e: 公钥指数
            n: RSA模数
            
        Returns:
            list of (k, d): 收敛项列表，其中 k/d 是 e/n 的近似
        """
        convergents = []
        
        # 初始化连分数展开
        quotients = []
        a, b = e, n
        
        # 欧几里得算法计算连分数系数
        while b != 0:
            q = a // b
            quotients.append(q)
            a, b = b, a - q * b
        
        # 从连分数系数计算收敛项
        h_prev2, h_prev1 = 0, 1
        k_prev2, k_prev1 = 1, 0
        
        for q in quotients:
            h = q * h_prev1 + h_prev2
            k = q * k_prev1 + k_prev2
            
            convergents.append((h, k))
            
            h_prev2, h_prev1 = h_prev1, h
            k_prev2, k_prev1 = k_prev1, k
        
        return convergents
    
    @staticmethod
    def rational_to_contfrac(x, y):
        """
        将有理数 x/y 转换为连分数表示
        
        Returns:
            list: 连分数系数列表 [a0, a1, a2, ...]
        """
        coefficients = []
        
        while y != 0:
            q = x // y
            coefficients.append(q)
            x, y = y, x - q * y
        
        return coefficients
    
    @staticmethod
    def contfrac_to_rational(coefficients):
        """
        将连分数系数转换回有理数
        
        Args:
            coefficients: 连分数系数列表
            
        Returns:
            (numerator, denominator): 分子和分母
        """
        if not coefficients:
            return (0, 1)
        
        num = 1
        denom = coefficients[-1]
        
        for i in range(len(coefficients) - 2, -1, -1):
            num, denom = denom, coefficients[i] * denom + num
        
        return (denom, num)

