# Wiener Attack - 快速开始指南

## 🚀 5分钟快速上手

### 1. 安装依赖

```bash
pip install pycryptodome
```

### 2. 运行简单测试

```bash
python test_simple.py
```

这将运行基本的Wiener攻击测试，验证实现是否正确。

**预期输出**：
```
✓ 攻击成功!
原始私钥: 12347
恢复私钥: 12347
匹配: ✓
耗时: ~1 ms
```

### 3. 运行综合演示

```bash
python demo.py
```

这将展示：
- 基本Wiener攻击
- 三种方法的边界对比
- 攻击方法实际对比
- 性能基准测试
- 理论分析
- 安全建议

### 4. 运行主程序

#### 单次攻击演示
```bash
# Wiener攻击
python main.py --mode single --bits 512 --attack wiener

# Bunder-Tonien攻击
python main.py --mode single --bits 512 --attack bunder_tonien

# 新边界攻击
python main.py --mode single --bits 512 --attack new_boundary
```

#### 三种方法对比
```bash
python main.py --mode compare --bits 1024
```

#### 基准测试（复现论文结果）
```bash
python main.py --mode benchmark
```

#### 边界测试
```bash
python main.py --mode boundary --bits 1024 --tests 5
```

## 📝 核心概念

### Wiener攻击原理

当RSA私钥 `d` 过小时，可以通过连分数方法恢复：

1. **计算** e/N 的连分数收敛项 k/d
2. **验证** 每个收敛项是否满足 ed ≡ 1 (mod φ(N))
3. **恢复** 完整的私钥

### 三种攻击方法的区别

| 方法 | 边界条件 | 适用范围 |
|------|---------|---------|
| Wiener (1990) | d < N^0.25 / 3 | 最严格 |
| Bunder-Tonien (2017) | d < 2√(2N) | 较宽松 |
| **新边界 (2023)** | d < √(8.24264N) | **最宽松** |

### 关键公式

**新边界推导**（论文 Lemma 3.1）：
```
α = 8 + 6√2 ≈ 16.4853
d < (α/2) × √N ≈ √(8.24264N)
```

## 🎯 使用场景

### 场景1: 教学演示

展示RSA在参数选择不当时的脆弱性：

```python
from wiener_attack import WienerAttack
from Crypto.Util.number import getPrime, inverse, GCD

# 生成弱RSA密钥
p = getPrime(256)
q = getPrime(256)
n = p * q
phi = (p - 1) * (q - 1)

# 使用小的d（不安全！）
d = 12345
while GCD(d, phi) != 1:
    d += 2

e = inverse(d, phi)

# 执行攻击
attacker = WienerAttack()
recovered_d = attacker.attack(e, n)

print(f"攻击{'成功' if recovered_d == d else '失败'}!")
```

### 场景2: 安全审计

检查RSA密钥是否易受Wiener攻击：

```python
from rsa_weak_key_generator import WeakRSAGenerator

gen = WeakRSAGenerator()

# 检查现有密钥
vulnerability = gen.check_vulnerability(n, d)

if vulnerability['wiener_vulnerable']:
    print("⚠ 警告: 密钥易受Wiener攻击!")
elif vulnerability['bunder_tonien_vulnerable']:
    print("⚠ 警告: 密钥易受Bunder-Tonien攻击!")
elif vulnerability['new_boundary_vulnerable']:
    print("⚠ 警告: 密钥易受新边界攻击!")
else:
    print("✓ 密钥安全")
```

### 场景3: 研究实验

复现论文结果：

```bash
# 运行基准测试
python main.py --mode benchmark

# 测试不同边界
python main.py --mode boundary --bits 1024 --tests 10
```

## 📊 性能参考

基于论文的实验结果（Intel i5-8265U + 4GB RAM）：

| RSA位长 | 耗时 |
|---------|------|
| 1024-bit | 0.052s |
| 2048-bit | 0.152s |
| 4096-bit | 0.75s |
| 8192-bit | 4.42s |

**时间复杂度**: O(log N)

## ⚠️ 安全警告

### 不要这样做

```python
# ❌ 错误：人为选择小的d
d = 12345
e = inverse(d, phi)  # 危险！
```

### 应该这样做

```python
# ✓ 正确：使用标准方法
e = 65537
d = inverse(e, phi)  # 安全

# 并确保 d 足够大
assert d > n ** 0.5
```

## 🔍 故障排除

### 问题1: 攻击失败

**原因**: d 可能不够小

**解决**: 
- 检查 d 是否满足边界条件
- 使用更小的 d 值进行测试

### 问题2: 浮点溢出

**原因**: N 太大导致浮点运算溢出

**解决**: 
- 代码已使用整数平方根避免此问题
- 如果仍有问题，请更新到最新版本

### 问题3: 性能慢

**原因**: 密钥太大或收敛项太多

**解决**:
- 使用较小的测试密钥（512-1024位）
- 确保 d 足够小

## 📚 进一步学习

### 推荐阅读

1. **Wiener原始论文** (1990)
   - "Cryptanalysis of short RSA secret exponents"
   - IEEE Transactions on Information Theory

2. **Bunder-Tonien论文** (2017)
   - "A new attack on the RSA cryptosystem based on continued fractions"

3. **新边界论文** (2023)
   - "A New Boundary of Minimum Private Key on Wiener Attack Against RSA Algorithm"
   - IEEE Conference on Cryptography and Network Security

### 相关主题

- Coppersmith方法
- 格基约简（LLL算法）
- 连分数理论
- RSA参数选择标准（NIST SP 800-56B）

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

本项目为NTU密码学课程作业，仅供学习交流使用。

---

**记住**: 本实现仅用于教育目的。在实际应用中，请始终使用经过验证的密码学库！

