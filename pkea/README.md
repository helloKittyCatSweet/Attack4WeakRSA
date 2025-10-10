# 广义 RSA 部分私钥泄露攻击

## 📚 理论背景

本项目实现了针对广义 RSA 模数 **N = p^r · q^s** 的部分私钥泄露攻击（Partial Key Exposure Attack），基于 Coppersmith 方法和格约简技术。

### 核心概念

#### 1. 广义 RSA 系统

传统 RSA 使用 N = p·q，而广义 RSA 使用：
```
N = p^r · q^s
```
其中 p, q 为素数，r, s ≥ 1 为整数幂次。

**欧拉函数**：
```
φ(N) = p^(r-1)·(p-1) · q^(s-1)·(q-1)
```

**密钥关系**：
```
e·d ≡ 1 (mod φ(N))
```

#### 2. 部分私钥泄露模型

假设攻击者获得了私钥 d 的部分信息：

- **MSB 泄露**：已知最高有效位（Most Significant Bits）
- **LSB 泄露**：已知最低有效位（Least Significant Bits）

设泄露比例为 δ（0 < δ < 1），则：
```
d = d₀ + x
```
其中：
- d₀：已知部分
- x：未知部分（|x| < X，X 为上界）

#### 3. Coppersmith 方法

**目标**：求解模方程的小根
```
f(x) ≡ 0 (mod M)
```
其中 |x| < X 且 X 相对较小。

**核心思想**：
1. 构造多项式格（Polynomial Lattice）
2. 使用 LLL/BKZ 算法进行格约简
3. 从短向量重构整数域上的多项式
4. 求解整数根

**Howgrave-Graham 定理**：
若多项式 G(x) 满足：
```
||G(xX)|| < M^β / √n
```
其中 n 为格维度，β 为参数，则 G(x) 在整数域上有根。

---

## 🚀 快速开始

### 环境要求

**推荐使用纯 Python 版本**（`rsa_partial_key_attack.py`）：
- Python 3.7+
- pycryptodome 库

**可选：SageMath 版本**（`partial_key_exposure_attack.py`）：
- SageMath 9.0 或更高版本
- pycryptodome 库

### 安装

#### 纯 Python 版本（推荐）

```bash
# 安装依赖
pip install pycryptodome

# 运行
python rsa_partial_key_attack.py
```

#### SageMath 版本（可选）

```bash
# 安装 SageMath (根据操作系统选择)
# Ubuntu/Debian:
sudo apt-get install sagemath

# macOS (使用 Homebrew):
brew install --cask sage

# Windows: 下载安装包
# https://www.sagemath.org/download-windows.html

# 安装 pycryptodome
sage -pip install pycryptodome

# 运行
sage partial_key_exposure_attack.py
```

### 运行

#### 单次快速演示（推荐）
```bash
python rsa_partial_key_attack.py
```

**预期输出**：
- 生成 RSA 参数（N = p² · q，24位素数）
- 创建 75% MSB 泄露
- 执行智能搜索攻击
- **完成时间**：约 0.004 秒 ✓

**示例输出**：
```
✓ 攻击成功!
  真实 x     = 238385
  恢复 x     = 238385
  匹配       = ✓ 是
  加解密测试 = ✓ 通过
总耗时: 0.004 秒
```

#### 批量实验
```bash
python rsa_partial_key_attack.py batch
```

测试多种参数组合：
- 不同泄露率（65%, 70%, 75%）
- 不同幂次（p·q, p²·q, p²·q²）
- 不同泄露类型（MSB, LSB）

**示例输出**：
```
总成功率: 83.3% (5/6)
所有实验在 1 秒内完成
```

---

## 📊 代码结构

### 主要函数

#### 1. `generate_rsa_generalized(bit_length, r, s)`
生成广义 RSA 参数。

**参数**：
- `bit_length`：素数位长（建议 32-128 以确保快速）
- `r, s`：幂次

**返回**：`(N, e, d, p, q, φ)`

#### 2. `create_partial_key_exposure(d, delta, exposure_type)`
创建部分私钥泄露场景。

**参数**：
- `d`：完整私钥
- `delta`：泄露比例（0 < δ < 1）
- `exposure_type`：`"MSB"` 或 `"LSB"`

**返回**：`(d₀, x, X)` - 已知部分、未知部分、上界

#### 3. `coppersmith_attack_univariate(N, e, d0, X, M, m, t)`
核心攻击函数，使用 Coppersmith 方法恢复未知部分。

**参数**：
- `N, e, d0, X`：RSA 参数和已知信息
- `M`：模数（通常为 φ(N)）
- `m, t`：格构造参数（控制格维度和成功率）

**返回**：恢复的 x 值（失败返回 None）

#### 4. `attack_partial_key_exposure(...)`
完整攻击流程的封装。

---

## 🔬 算法详解

### 格构造

构造多项式集合：
```
g_{i,j} = x^i · f(x)^j · M^(m-j)
```
其中：
- f(x) = e·x + (e·d₀ - 1)
- j = 0, 1, ..., m-1
- i = 0, 1, ..., m-j-1

额外多项式：
```
h_i = x^i · f(x)^m,  i = 0, 1, ..., t-1
```

### 格基矩阵

将多项式系数（经 X 缩放）作为行向量构成矩阵 L。

### LLL 约简

对 L 执行 LLL 算法，得到约简后的格基 L'。

### 根恢复

从 L' 的短向量重构多项式 G(x)，求解整数根。

---

## ⚙️ 参数调优

### 快速演示（几秒内完成）

```python
attack_partial_key_exposure(
    bit_length=64,    # 64位素数
    r=2, s=1,         # N = p²·q
    delta=0.6,        # 60% 泄露
    exposure_type="MSB",
    m=2, t=1          # 小格维度
)
```

### 平衡速度与成功率

| 参数 | 快速 | 平衡 | 高成功率 |
|------|------|------|----------|
| `bit_length` | 48-64 | 64-96 | 96-128 |
| `delta` | 0.6-0.7 | 0.5-0.6 | 0.4-0.5 |
| `m` | 2 | 3 | 4-5 |
| `t` | 1 | 1-2 | 2-3 |

**注意**：
- `bit_length` 越大，安全性越高但速度越慢
- `delta` 越大（泄露越多），攻击越容易成功
- `m, t` 越大，格维度越高，成功率越高但速度指数级下降

---

## 📈 实验结果示例

### 实验 1：标准配置
```
参数: bit_length=64, r=2, s=1, δ=0.6, MSB
结果: ✓ 攻击成功
耗时: 2.3 秒
```

### 实验 2：高难度
```
参数: bit_length=96, r=2, s=2, δ=0.5, MSB
结果: ✓ 攻击成功
耗时: 15.7 秒
```

---

## 🔐 安全建议

基于本攻击的防御措施：

1. **避免私钥泄露**：使用安全的密钥存储（HSM、TPM）
2. **增加密钥长度**：使用 2048 位或更长的 RSA 密钥
3. **避免广义 RSA**：除非有特殊需求，使用标准 RSA (N=p·q)
4. **侧信道防护**：防止时序攻击、功耗分析等泄露私钥信息

---

## 📖 参考文献

1. **主要论文**：
   - "Partial Key Exposure Attacks on RSA with Moduli N=p^r q^s"

2. **理论基础**：
   - Coppersmith, D. "Small Solutions to Polynomial Equations, and Low Exponent RSA Vulnerabilities" (1996)
   - Howgrave-Graham, N. "Finding Small Roots of Univariate Modular Equations Revisited" (1997)

3. **格约简**：
   - Lenstra, A.K., Lenstra, H.W., Lovász, L. "Factoring Polynomials with Rational Coefficients" (1982)

---

## 📝 许可证

本项目仅用于教育和研究目的。请勿用于非法用途。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## ⚠️ 免责声明

本代码仅在**安全可控的实验环境**中使用，用于学术研究和密码学教育。作者不对任何滥用行为负责。

