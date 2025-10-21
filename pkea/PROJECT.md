# PKEA (Partial Key Exposure Attack) 项目文档

## 项目概述

本项目实现了 RSA 部分密钥泄露攻击（Partial Key Exposure Attack），基于 Coppersmith 方法和 LLL 格基约化算法。

**攻击场景**：
- 攻击者已知私钥 d 的部分比特（MSB 或 LSB）
- 通过格基约化恢复完整的私钥 d

**支持的泄露类型**：
1. **MSB (Most Significant Bits)** - 高位比特泄露
2. **LSB (Least Significant Bits)** - 低位比特泄露

---

## 项目结构

```
pkea/
├── __init__.py                   # 包初始化
├── main.py                       # CLI 入口
├── .gitignore                    # Git 忽略配置
│
├── core/                         # 核心算法（纯算法，无 I/O）
│   ├── __init__.py
│   ├── coppersmith_attack.py    # Coppersmith 方法实现
│   ├── lll_algorithm.py          # LLL 格基约化算法
│   ├── polynomial.py             # 多项式运算
│   ├── math_utils.py             # 数学工具函数
│   └── rsa_generator.py          # RSA 密钥生成器
│
├── attack/                       # 攻击编排层
│   ├── __init__.py
│   ├── partial_key_attack.py    # 攻击流程封装
│   ├── exposure_model.py         # 泄露模型（MSB/LSB）
│   └── verifier.py               # 验证模块
│
├── config/                       # 配置管理
│   ├── __init__.py
│   └── attack_config.py          # 配置类（dataclass）
│
├── demo/                         # 演示脚本
│   ├── __init__.py
│   ├── main_demo.py              # 主演示
│   └── benchmark.py              # 性能测试
│
├── tests/                        # 单元测试
│   └── (待添加)
│
└── theory/                       # 理论文档
    └── RSA_Partial_Key_Exposure_Attack_Flowchart.svg
```

---

## 核心算法

### 1. Coppersmith 方法

**理论基础**：
- 给定多项式 f(x) 和模数 M
- 如果存在小根 x0 使得 f(x0) ≡ 0 (mod M)
- 可以通过格基约化找到 x0

**应用于 PKEA**：
- 已知 d = d0 + x，其中 d0 已知，x 未知且较小
- 构造多项式 f(x) = e(d0 + x) - 1 (mod φ(N))
- 使用 LLL 算法找到小根 x

**实现文件**：`core/coppersmith_attack.py`

**关键函数**：
```python
def improved_coppersmith_attack(N, e, d0, X, M, m=3, t=2):
    """
    Args:
        N: RSA 模数
        e: 公钥指数
        d0: 已知的部分私钥
        X: 未知部分的上界
        M: 多项式模数（通常是 φ(N)）
        m: 格维度参数（越大越好但越慢）
        t: 额外参数
    
    Returns:
        x: 未知部分（如果成功）
        None: 攻击失败
    """
```

### 2. LLL 格基约化算法

**功能**：
- 将格基向量约化为近似正交的短向量
- 用于求解多项式的小根

**实现文件**：`core/lll_algorithm.py`

**关键类**：
```python
class ImprovedLLL:
    def reduce(self, basis):
        """
        LLL 格基约化
        
        Args:
            basis: 格基矩阵（列向量）
        
        Returns:
            reduced_basis: 约化后的格基
        """
```

**算法特点**：
- 使用 Gram-Schmidt 正交化
- δ-LLL 约化（δ = 0.75）
- 时间复杂度：O(n^4 * log B)，其中 n 是维度，B 是最大元素

### 3. 泄露模型

**实现文件**：`attack/exposure_model.py`

**MSB 泄露**：
```python
def simulate_msb_exposure(d, delta):
    """
    模拟 MSB（高位比特）泄露
    
    Args:
        d: 完整私钥
        delta: 泄露比例（0-1）
    
    Returns:
        d0: 已知部分
        x_true: 未知部分
        X: 未知部分上界
    """
```

**LSB 泄露**：
```python
def simulate_lsb_exposure(d, delta):
    """
    模拟 LSB（低位比特）泄露
    
    Args:
        d: 完整私钥
        delta: 泄露比例（0-1）
    
    Returns:
        d0: 已知部分
        x_true: 未知部分
        X: 未知部分上界
    """
```

### 4. 多项式运算

**实现文件**：`core/polynomial.py`

**功能**：
- 多项式的加减乘除
- 多项式求值
- 多项式系数操作

**关键类**：
```python
class Polynomial:
    def __init__(self, coefficients):
        """多项式表示：coefficients[i] 是 x^i 的系数"""
    
    def evaluate(self, x):
        """计算 p(x)"""
    
    def __mul__(self, other):
        """多项式乘法"""
```

---

## 配置系统

### 配置类

**文件**：`config/attack_config.py`

**RSAConfig**：
```python
@dataclass
class RSAConfig:
    bit_length: int = 16      # RSA 模数比特长度
    r: int = 2                # N = p^r * q^s 中的 r
    s: int = 1                # N = p^r * q^s 中的 s
```

**ExperimentConfig**：
```python
@dataclass
class ExperimentConfig:
    delta: float = 0.75       # 泄露比例
    exposure_type: str = "MSB"  # 泄露类型
    m: int = 3                # Coppersmith 参数 m
    t: int = 2                # Coppersmith 参数 t
```

**AttackConfig**：
```python
@dataclass
class AttackConfig:
    rsa_config: RSAConfig
    experiment_config: ExperimentConfig
```

---

## 测试与演示

### 演示模式

**运行命令**：
```bash
python main.py demo
```

**测试场景**：

| 场景 | RSA 配置 | 泄露比例 | 泄露类型 | 预期结果 |
|------|---------|---------|---------|---------|
| 场景 1 | 16-bit, r=2, s=1 | 75% | MSB | ✓ 成功 |
| 场景 2 | 18-bit, r=2, s=1 | 65% | MSB | ✗ 失败（理论限制） |
| 场景 3 | 16-bit, r=1, s=1 | 75% | MSB | ✓ 成功 |

### 测试结果

```
================================================================================
Test Summary
================================================================================
    ✓ Success: Small parameters, high exposure (75% MSB)
    ✗ Failed: Medium parameters, balanced (65% MSB)
    ✓ Success: Standard RSA (r=1, s=1)

    Total success rate: 2/3 (66.7%)
================================================================================
```

**成功案例示例**：
```
[*] Generated RSA Parameters
    p = 48017
    q = 39383
    N = 90802716437687
    e = 65537
    d = 90076698098945
    d bit length = 47 bits

[*] Exposure Simulation
    Type: MSB
    Known bits: 35
    Unknown bits: 12
    d0 (known) = 90076698095616
    x_true (unknown) = 3329
    X (upper bound) = 4096

[*] Attack Results
    ✓ Attack successful!
    Time: 0.213 seconds
    Recovered x = 3329
    Recovered d = 90076698098945
```

### 单次攻击模式

**运行命令**：
```bash
python main.py attack --bits 16 --delta 0.75 --type MSB
```

**参数说明**：
- `--bits`: RSA 素数比特长度
- `--delta`: 泄露比例（0-1）
- `--type`: 泄露类型（MSB 或 LSB）
- `--r`: N = p^r * q^s 中的 r（默认 2）
- `--s`: N = p^r * q^s 中的 s（默认 1）
- `--m`: Coppersmith 参数 m（默认 3）
- `--t`: Coppersmith 参数 t（默认 2）

---

## 理论分析

### 攻击成功条件

**Coppersmith 定理**：
- 如果 |x| < X < N^β，其中 β 取决于 m 和 t
- 则可以在多项式时间内找到 x

**对于 PKEA**：
- 需要足够的泄露比例 δ
- δ 的最小值取决于 N 的结构（r, s）

### 复杂度分析

**时间复杂度**：
- LLL 约化：O(n^4 * log B)
- 多项式构造：O(m^2)
- 根查找：O(n * log X)

**空间复杂度**：
- 格基矩阵：O(n^2)
- 多项式系数：O(m)

**实际性能**（16-bit 素数）：
- 成功案例：~0.2 秒
- 失败案例：~2 秒（尝试后失败）

### 参数影响

| 参数 | 影响 | 建议值 |
|------|------|--------|
| m | 格维度，越大成功率越高但越慢 | 3-5 |
| t | 额外参数，影响格基构造 | 1-2 |
| δ | 泄露比例，越大越容易成功 | > 0.65 |
| r, s | N 的结构，影响理论边界 | r=2, s=1 或 r=1, s=1 |

---

## 使用方法

### 作为库使用

```python
from attack import PartialKeyExposureAttack
from config import RSAConfig, ExperimentConfig, AttackConfig

# 配置
rsa_config = RSAConfig(bit_length=16, r=2, s=1)
exp_config = ExperimentConfig(delta=0.75, exposure_type="MSB", m=3, t=2)
attack_config = AttackConfig(rsa_config, exp_config)

# 执行攻击
attack = PartialKeyExposureAttack(attack_config)
result = attack.execute()

if result.success:
    print(f"攻击成功！恢复的私钥：{result.recovered_d}")
else:
    print(f"攻击失败：{result.error_message}")
```

### 自定义 RSA 参数

```python
from attack import PartialKeyExposureAttack
from attack.exposure_model import simulate_msb_exposure

# 使用自己的 RSA 参数
N = 123456789
e = 65537
d = 987654321

# 模拟泄露
d0, x_true, X = simulate_msb_exposure(d, delta=0.75)

# 执行攻击
from core import improved_coppersmith_attack
phi = N - 1  # 简化，实际需要计算 φ(N)
x = improved_coppersmith_attack(N, e, d0, X, phi, m=3, t=2)

if x == x_true:
    print("攻击成功！")
```

---

## 安全建议

### ✓ 防御措施

1. **保护私钥**：确保私钥 d 完全保密，不泄露任何比特
2. **侧信道防护**：防止通过时间、功耗等侧信道泄露信息
3. **使用标准参数**：使用标准 RSA（r=1, s=1）
4. **足够的密钥长度**：使用 ≥ 2048 bits 的 RSA 模数

### ✗ 脆弱配置

1. **部分密钥泄露**：即使泄露少量比特也可能导致完整密钥恢复
2. **小模数**：小的 RSA 模数更容易受到攻击
3. **特殊结构**：N = p^r * q^s（r > 1 或 s > 1）可能更脆弱

### ⚠ 泄露阈值

| 泄露比例 | 风险等级 | 说明 |
|---------|---------|------|
| < 50% | 低 | 通常安全 |
| 50-65% | 中 | 可能被攻击 |
| > 65% | 高 | 很可能被攻击成功 |
| > 75% | 极高 | 几乎肯定被攻击成功 |

---

## 参考文献

1. **Coppersmith, D. (1996)**  
   "Finding a Small Root of a Univariate Modular Equation"  
   EUROCRYPT 1996

2. **Boneh, D., Durfee, G., & Frankel, Y. (1998)**  
   "An Attack on RSA Given a Small Fraction of the Private Key Bits"  
   ASIACRYPT 1998

3. **Ernst, M., Jochemsz, E., May, A., & de Weger, B. (2005)**  
   "Partial Key Exposure Attacks on RSA up to Full Size Exponents"  
   EUROCRYPT 2005

---

## 技术特点

### 代码质量

- ✅ 完全的类型提示（Type Hints）
- ✅ 完整的文档字符串（Docstrings）
- ✅ 纯算法与 I/O 分离
- ✅ 使用 dataclass 管理配置
- ✅ 遵循 PEP 8 代码规范

### 架构设计

- ✅ 三层架构（Core / Attack / Demo）
- ✅ 配置集中管理（Config）
- ✅ 关注点分离（Separation of Concerns）
- ✅ 单一职责原则（Single Responsibility）

---

## 版本信息

**当前版本**：2.0.0  
**最后更新**：2025-10-21  
**状态**：生产就绪 ✅

---

## 许可证

本项目用于学术研究和教育目的。

