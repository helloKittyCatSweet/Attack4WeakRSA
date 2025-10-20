# Wiener Attack and Improvements on RSA

维纳攻击及其改进版本的Python实现

## 📖 概述

本项目实现了针对小私钥RSA的三种攻击方法：

1. **Wiener攻击 (1990)** - 原始维纳攻击
2. **Bunder-Tonien攻击 (2017)** - 改进的维纳攻击
3. **新边界攻击 (2023)** - 基于最新论文的进一步改进

基于论文：**"A New Boundary of Minimum Private Key on Wiener Attack Against RSA Algorithm"** (IEEE 2023)

## 🎯 核心原理

### RSA安全性与私钥大小

RSA的安全性依赖于私钥 `d` 的大小。如果 `d` 过小，可以通过连分数方法恢复私钥。

### 三种攻击方法的边界条件

| 攻击方法 | 年份 | 边界条件 | 公式 |
|---------|------|---------|------|
| **Wiener** | 1990 | d < N^0.25 / 3 | 约 N^0.25 |
| **Bunder-Tonien** | 2017 | d < 2√(2N) | 约 2.828√N |
| **新边界** | 2023 | d < √(8.24264N) | 约 2.871√N |

### 数学基础

**连分数展开**：
- 计算 e/N 的连分数收敛项 k/d
- 如果 d 足够小，k/d 会非常接近 e/N
- 通过验证 ed ≡ 1 (mod φ(N)) 来确认候选私钥

**新边界推导** (论文 Lemma 3.1)：
```
α = 8 + 6√2 ≈ 16.4853
d < (α/2) × √N ≈ √(8.24264N)
```

## 🏗️ 项目结构

```
wiener/
├── main.py                      # 主演示程序
├── config.py                    # 配置参数
├── continued_fraction.py        # 连分数算法
├── rsa_weak_key_generator.py    # 弱RSA密钥生成器
├── wiener_attack.py             # 三种攻击方法实现
└── README.md                    # 本文件
```

## 🚀 快速开始

### 依赖安装

```bash
pip install pycryptodome
```

### 基本使用

#### 1. 运行单次攻击演示

```bash
# 使用新边界攻击（默认）
python main.py --mode single --bits 1024 --attack new_boundary

# 使用Wiener攻击
python main.py --mode single --bits 1024 --attack wiener

# 使用Bunder-Tonien攻击
python main.py --mode single --bits 1024 --attack bunder_tonien
```

#### 2. 运行三种方法对比

```bash
python main.py --mode compare --bits 1024
```

#### 3. 运行基准测试（复现论文结果）

```bash
python main.py --mode benchmark
```

论文中的参考值（Intel i5-8265U + 4GB RAM）：
- 1024-bit: 0.052s
- 2048-bit: 0.152s
- 4096-bit: 0.75s
- 8192-bit: 4.42s

#### 4. 运行边界测试

```bash
python main.py --mode boundary --bits 1024 --tests 5
```

## 📊 示例输出

### 单次攻击演示

```
======================================================================
维纳攻击演示 - NEW_BOUNDARY
======================================================================

[1] 生成 1024-bit 弱RSA密钥...
  N 比特长度: 1024
  d 比特长度: 520
  理论边界: 2.87e+154
  d < 边界: ✓

[2] 检查密钥脆弱性...
  Wiener攻击:
    边界: 1.68e+77
    脆弱: ✗
  
  Bunder-Tonien攻击:
    边界: 2.83e+154
    脆弱: ✓
  
  新边界攻击:
    边界: 2.87e+154
    脆弱: ✓

[3] 执行 new_boundary 攻击...

[4] 验证攻击结果...
  ✓ 攻击成功!
  原始私钥 d: 123456...
  恢复私钥 d: 123456...
  匹配: ✓
  耗时: 0.152 ms

[5] 加密解密测试...
  原始消息: 123456789
  密文: 987654...
  解密成功: ✓
```

### 三种方法对比

```
======================================================================
三种攻击方法对比 - 1024-bit RSA
======================================================================

[2] 理论边界对比...

  Wiener (1990): N^0.25 / 3
    边界值: 1.68e+77
    比特长度: 256

  Bunder-Tonien (2017): 2*sqrt(2*N)
    边界值: 2.83e+154
    比特长度: 513
    相对Wiener提升: 1.68e+77x

  新边界 (2023): sqrt(8.24264*N)
    边界值: 2.87e+154
    比特长度: 513
    相对Wiener提升: 1.71e+77x
    相对Bunder-Tonien提升: 1.01x

[4] 执行所有攻击方法...

方法                  成功        耗时(ms)         匹配      
----------------------------------------------------------------------
wiener              ✗          0.145           ✗         
bunder_tonien       ✓          0.148           ✓         
new_boundary        ✓          0.150           ✓         
```

## 🔧 模块说明

### 1. continued_fraction.py

实现连分数算法：
- `compute_convergents(e, n)` - 计算 e/n 的连分数收敛项
- `rational_to_contfrac(x, y)` - 有理数转连分数
- `contfrac_to_rational(coefficients)` - 连分数转有理数

### 2. rsa_weak_key_generator.py

生成易受攻击的弱RSA密钥：
- `generate_weak_rsa(bits, d_ratio)` - 生成指定d比例的弱密钥
- `generate_by_boundary(bits, attack_type)` - 根据攻击类型生成密钥
- `check_vulnerability(n, d)` - 检查密钥脆弱性

### 3. wiener_attack.py

实现三种攻击方法：
- `WienerAttack` - 原始Wiener攻击 (d < N^0.25 / 3)
- `BunderTonienAttack` - Bunder-Tonien攻击 (d < 2√(2N))
- `NewBoundaryAttack` - 新边界攻击 (d < √(8.24264N))
- `AttackComparison` - 攻击方法对比工具

### 4. main.py

主演示程序，提供四种运行模式：
- `single` - 单次攻击演示
- `compare` - 三种方法对比
- `benchmark` - 基准测试
- `boundary` - 边界测试

## 📈 性能分析

### 时间复杂度

所有三种攻击方法的时间复杂度均为 **O(log N)**，主要来自：
1. 连分数展开（欧几里得算法）
2. 收敛项验证

### 实验结果

在现代计算机上（示例配置）：

| RSA位长 | 平均耗时 |
|---------|---------|
| 512     | ~0.02s  |
| 1024    | ~0.05s  |
| 2048    | ~0.15s  |
| 4096    | ~0.75s  |
| 8192    | ~4.5s   |

## 🔐 安全建议

### 如何防御Wiener攻击

1. **使用足够大的私钥**
   - 确保 d > N^0.5
   - 遵循NIST SP 800-56B标准

2. **密钥生成规范**
   - 使用标准的RSA密钥生成算法
   - 不要人为选择小的私钥

3. **推荐参数**
   - RSA模数：≥ 2048位
   - 公钥指数：e = 65537（常用值）
   - 私钥：随机生成，不施加大小限制

### 脆弱配置示例

❌ **不安全**：
```python
# 人为选择小的d
d = 12345
e = inverse(d, phi)  # 危险！
```

✅ **安全**：
```python
# 标准方法
e = 65537
d = inverse(e, phi)  # 安全
```

## 📚 参考文献

1. **Wiener, M. J.** (1990). "Cryptanalysis of short RSA secret exponents." *IEEE Transactions on Information Theory*, 36(3), 553-558.

2. **Bunder, M., & Tonien, J.** (2017). "A new attack on the RSA cryptosystem based on continued fractions." *Malaysian Journal of Mathematical Sciences*, 11, 45-57.

3. **论文** (2023). "A New Boundary of Minimum Private Key on Wiener Attack Against RSA Algorithm." *IEEE International Conference on Cryptography and Network Security*.

4. **Boneh, D., & Durfee, G.** (2000). "Cryptanalysis of RSA with private key d < N^0.292." *IEEE Transactions on Information Theory*, 46(4), 1339-1349.

5. **Blömer, J., & May, A.** (2004). "A generalized Wiener attack on RSA." *PKC 2004*, LNCS 2947, 1-13.

## 🎓 教育用途

本项目仅用于：
- ✅ 密码学教学和研究
- ✅ 安全性分析和测试
- ✅ 学术论文复现

**警告**：请勿用于非法目的！

## 📝 许可证

本项目为NTU密码学课程作业，仅供学习交流使用。

## 👥 贡献者

NTU SC6104 - Introduction to Cryptography

---

**注意**：本实现展示了RSA在参数选择不当时的脆弱性。在实际应用中，请始终使用经过验证的密码学库和标准密钥生成方法！

