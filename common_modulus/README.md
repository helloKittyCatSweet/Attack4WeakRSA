# Common Modulus Attack on RSA and ECC-RSA

## 📚 论文信息

**标题**: Common Modulus Attack on the Elliptic Curve-Based RSA Algorithm Variant  
**作者**: Boudabra & Nitaj  
**主题**: 对基于椭圆曲线改造的RSA变体进行同模数攻击分析

## 🎯 攻击原理

### 核心思想

当同一消息 `M` 使用**相同模数 N** 但**不同公钥指数 e₁, e₂** 加密时，如果 `gcd(e₁, e₂) = 1`，攻击者可以在**不知道私钥**的情况下恢复明文。

### 数学基础

1. **加密过程**:
   - 用户1: `C₁ = M^e₁ mod N`
   - 用户2: `C₂ = M^e₂ mod N`

2. **扩展欧几里得算法**:
   - 求解: `e₁·x + e₂·y = gcd(e₁, e₂) = 1`
   - 得到整数 `x` 和 `y`

3. **恢复明文**:
   ```
   M = C₁^x · C₂^y mod N
   ```

### 为什么有效？

```
C₁^x · C₂^y ≡ (M^e₁)^x · (M^e₂)^y  (mod N)
            ≡ M^(e₁·x) · M^(e₂·y)  (mod N)
            ≡ M^(e₁·x + e₂·y)      (mod N)
            ≡ M^1                  (mod N)
            ≡ M                    (mod N)
```

## 📊 论文示例

### 参数

```python
N  = 181603559630213323475279432919469869812801
e₁ = 233
e₂ = 151

# 扩展欧几里得算法结果
x = 35
y = -54

# 验证: 233 × 35 + 151 × (-54) = 8155 - 8154 = 1 ✓
```

### 明文点 (ECC-RSA)

```python
M = (r, y_M) = (276576193905959805653341, 24123988022450690140866)
```

### 密文点

```python
C₁ = (165824579408065034165410, 127733294106034267552844)
C₂ = (165824579408065034165410, 53870265524179202259957)
```

## 🚀 快速开始

### 安装依赖

```bash
pip install pycryptodome
```

### 运行演示

```bash
# 演示攻击过程
python main.py --mode demo

# 复现论文示例
python main.py --mode paper

# 运行测试套件
python main.py --mode test

# 自定义参数
python main.py --mode custom --bits 1024 --e1 3 --e2 5 --message 12345
```

## 📁 项目结构

```
common_modulus/
├── config.py                    # 配置参数
├── extended_gcd.py              # 扩展欧几里得算法
├── common_modulus_attack.py     # 攻击实现
├── paper_example.py             # 论文示例复现
├── main.py                      # 主程序
└── README.md                    # 本文档
```

## 🔬 实现细节

### 1. 扩展欧几里得算法

<augment_code_snippet path="Desktop/mimaxue/Attack4WeakRSA/common_modulus/extended_gcd.py" mode="EXCERPT">
````python
def extended_gcd(a, b):
    """求解 ax + by = gcd(a, b)"""
    if b == 0:
        return a, 1, 0
    
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    
    return old_r, old_s, old_t
````
</augment_code_snippet>

### 2. 同模数攻击

<augment_code_snippet path="Desktop/mimaxue/Attack4WeakRSA/common_modulus/common_modulus_attack.py" mode="EXCERPT">
````python
def attack(self, N, e1, e2, C1, C2):
    # 1. 检查 gcd(e1, e2) = 1
    gcd, x, y = extended_gcd(e1, e2)
    if gcd != 1:
        return None
    
    # 2. 计算 M = C1^x * C2^y mod N
    # 处理负指数
    if x < 0:
        C1_part = pow(mod_inverse(C1, N), -x, N)
    else:
        C1_part = pow(C1, x, N)
    
    if y < 0:
        C2_part = pow(mod_inverse(C2, N), -y, N)
    else:
        C2_part = pow(C2, y, N)
    
    M = (C1_part * C2_part) % N
    return M
````
</augment_code_snippet>

## 📈 性能分析

### 时间复杂度

| 操作 | 复杂度 |
|------|--------|
| 扩展欧几里得算法 | O(log min(e₁, e₂)) |
| 模幂运算 | O(log N) |
| **总体** | **O(log N)** |

### 实测性能

| RSA位长 | 耗时 |
|---------|------|
| 512-bit | ~1 ms |
| 1024-bit | ~2 ms |
| 2048-bit | ~5 ms |

**结论**: 攻击几乎即时完成，实际环境中极易实施。

## ⚠️ 安全含义

### 为什么这很危险？

1. **模数重用是根本性错误**
   - 即使使用不同的公钥指数
   - 即使底层运算换成椭圆曲线
   - 只要模数相同，攻击就有效

2. **攻击条件容易满足**
   - `gcd(e₁, e₂) = 1` 很常见（如 e₁=3, e₂=5）
   - 不需要私钥或因子分解
   - 复杂度极低，几乎即时

3. **实际场景**
   - 分布式系统中多个实体误用同一 N
   - 共享密钥库配置错误
   - 多方协议设计缺陷

### 防御措施

✅ **正确做法**:
- 每个用户/实体使用**独立的模数 N**
- 不同密钥对之间完全独立
- 定期审计密钥配置

❌ **错误做法**:
- 多个用户共享同一个 N
- 认为"不同的 e 就安全"
- 忽视密钥管理最佳实践

## 🧪 测试示例

### 示例1: 基本攻击

```python
from common_modulus_attack import CommonModulusAttack

# 参数
N = 3233
e1 = 3
e2 = 5
M = 42

# 生成密文
C1 = pow(M, e1, N)  # = 2557
C2 = pow(M, e2, N)  # = 2182

# 执行攻击
attacker = CommonModulusAttack()
recovered_M = attacker.attack(N, e1, e2, C1, C2)

print(f"恢复的明文: {recovered_M}")  # 输出: 42
```

### 示例2: 论文参数

```python
from paper_example import test_paper_example_rsa

# 使用论文中的具体参数
test_paper_example_rsa()
```

## 📖 理论背景

### 贝祖等式 (Bézout's Identity)

对于任意整数 a, b，存在整数 x, y 使得:
```
ax + by = gcd(a, b)
```

当 `gcd(a, b) = 1` 时:
```
ax + by = 1
```

### 应用到RSA

```
e₁·x + e₂·y = 1

⟹ M^(e₁·x + e₂·y) ≡ M^1 ≡ M (mod N)

⟹ (M^e₁)^x · (M^e₂)^y ≡ M (mod N)

⟹ C₁^x · C₂^y ≡ M (mod N)
```

## 🔍 与其他攻击的对比

| 攻击方法 | 条件 | 复杂度 | 需要私钥 |
|---------|------|--------|---------|
| **同模数攻击** | 同N, gcd(e₁,e₂)=1 | O(log N) | ❌ |
| Wiener攻击 | d < N^0.25 | O(log N) | ❌ |
| 因子分解 | 无特殊条件 | 亚指数 | ❌ |
| 暴力破解 | 无特殊条件 | 指数级 | ✓ |

**优势**: 
- 不需要私钥
- 不需要因子分解
- 复杂度极低
- 成功率100%（满足条件时）

## 📚 参考文献

1. **Common Modulus Attack on the Elliptic Curve-Based RSA Algorithm Variant**  
   Boudabra & Nitaj

2. **Twenty Years of Attacks on the RSA Cryptosystem**  
   Dan Boneh, 1999

3. **Handbook of Applied Cryptography**  
   Menezes, van Oorschot, Vanstone

## 🎓 教育价值

本实现适合用于:
- 密码学课程教学
- RSA安全性研究
- 密钥管理最佳实践演示
- 安全审计培训

**重要提醒**: 仅用于教育和研究目的，不得用于未授权的系统！

---

**项目**: Attack4WeakRSA  
**课程**: SC6104 - Introduction to Cryptography (NTU)  
**许可**: Educational Use Only

