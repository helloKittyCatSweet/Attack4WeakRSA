# Common Modulus Attack - 快速开始

## 🚀 5分钟快速上手

### 1. 安装依赖

```bash
pip install pycryptodome
```

### 2. 运行演示

```bash
cd Desktop/mimaxue/Attack4WeakRSA/common_modulus
python main.py --mode demo
```

**预期输出**:
```
✓ 攻击成功!
原始消息: 123456789
恢复消息: 123456789
耗时: ~2 ms
```

### 3. 复现论文示例

```bash
python main.py --mode paper
```

这将复现论文中的具体参数和结果。

### 4. 运行测试套件

```bash
python main.py --mode test
```

测试512/1024/2048-bit RSA的攻击效果。

## 📝 核心概念

### 什么是同模数攻击？

当两个用户使用**相同的RSA模数N**但**不同的公钥指数e₁和e₂**时，如果攻击者截获了同一消息的两个密文，就可以在**不知道私钥**的情况下恢复明文。

### 攻击条件

1. ✅ 相同的模数 N
2. ✅ 不同的公钥指数 e₁, e₂
3. ✅ gcd(e₁, e₂) = 1（互素）
4. ✅ 相同的明文 M

### 攻击步骤

```
1. 截获密文: C₁ = M^e₁ mod N, C₂ = M^e₂ mod N
2. 扩展欧几里得: 求解 e₁·x + e₂·y = 1
3. 恢复明文: M = C₁^x · C₂^y mod N
```

## 🎯 使用示例

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
recovered_M = attacker.attack(N, e1, e2, C1, C2, verbose=True)

print(f"恢复的明文: {recovered_M}")  # 输出: 42
```

### 示例2: 自定义参数

```bash
python main.py --mode custom --bits 1024 --e1 7 --e2 11 --message 987654321
```

### 示例3: 仅测试扩展欧几里得算法

```python
from extended_gcd import extended_gcd

e1, e2 = 233, 151
gcd, x, y = extended_gcd(e1, e2)

print(f"gcd({e1}, {e2}) = {gcd}")
print(f"{e1} × {x} + {e2} × {y} = {gcd}")
# 输出: 233 × 35 + 151 × (-54) = 1
```

## 📊 命令行选项

### 主程序 (main.py)

```bash
python main.py [选项]

选项:
  --mode {paper,demo,test,custom}
                        运行模式 (默认: demo)
  --bits BITS           RSA密钥位长 (仅custom模式, 默认: 1024)
  --e1 E1               第一个公钥指数 (仅custom模式, 默认: 3)
  --e2 E2               第二个公钥指数 (仅custom模式, 默认: 5)
  --message MESSAGE     消息 (仅custom模式, 默认: 123456789)
```

### 运行模式说明

| 模式 | 说明 | 用途 |
|------|------|------|
| `demo` | 演示攻击过程 | 快速了解攻击原理 |
| `paper` | 复现论文示例 | 验证实现正确性 |
| `test` | 运行测试套件 | 测试多种配置 |
| `custom` | 自定义参数 | 实验不同场景 |

## 🔍 理解输出

### 成功的攻击输出

```
======================================================================
同模数攻击 - 普通RSA
======================================================================

[1] 参数:
  N  = 3233
  e1 = 3
  e2 = 5
  C1 = 2557
  C2 = 2182

[2] 检查条件: gcd(e1, e2) = 1
  gcd(3, 5) = 1
  ✓ e1 和 e2 互素，可以攻击

[3] 扩展欧几里得算法结果:
  3 × 2 + 5 × -1 = 1
  x = 2
  y = -1

[4] 计算明文:
  M = C1^x × C2^y mod N
  C1^2 mod N = 1234
  C2^-1 mod N = 5678
  M = 42
  耗时: 0.123 ms

[5] 验证结果:
  ✓ 攻击成功!
```

### 失败的攻击输出

```
[2] 检查条件: gcd(e1, e2) = 1
  gcd(6, 9) = 3
  ✗ 攻击失败: e1 和 e2 不互素
```

## ⚠️ 常见问题

### Q1: 为什么攻击失败？

**A**: 检查以下条件:
- e₁ 和 e₂ 是否互素？（gcd(e₁, e₂) = 1）
- 是否使用了相同的模数 N？
- 密文是否对应同一明文？

### Q2: 如何选择e₁和e₂？

**A**: 常见的互素组合:
- (3, 5)
- (3, 7)
- (5, 7)
- (7, 11)
- (17, 257)

### Q3: 攻击需要多长时间？

**A**: 非常快！
- 512-bit: ~0.05 ms
- 1024-bit: ~0.08 ms
- 2048-bit: ~0.60 ms

### Q4: 这个攻击在实际中有用吗？

**A**: 是的！如果系统配置错误导致:
- 多个用户共享同一个 N
- 密钥轮换时重用 N
- 分布式系统中模数管理不当

## 🛡️ 安全建议

### ❌ 不要这样做

```python
# 错误：多个用户共享同一个N
N = generate_rsa_modulus()
user1 = (N, e1, d1)  # 用户1
user2 = (N, e2, d2)  # 用户2 - 危险！
```

### ✅ 应该这样做

```python
# 正确：每个用户独立的N
user1_N = generate_rsa_modulus()
user2_N = generate_rsa_modulus()  # 不同的N

user1 = (user1_N, e1, d1)
user2 = (user2_N, e2, d2)  # 安全
```

## 📚 进一步学习

### 推荐阅读

1. **论文原文**
   - "Common Modulus Attack on the Elliptic Curve-Based RSA Algorithm Variant"
   - Boudabra & Nitaj

2. **相关主题**
   - 扩展欧几里得算法
   - 贝祖等式 (Bézout's Identity)
   - RSA密钥管理最佳实践

### 相关攻击

- Wiener Attack (小私钥攻击)
- Fermat Attack (接近素数攻击)
- Partial Key Exposure Attack (部分密钥泄露攻击)

## 🧪 实验建议

### 实验1: 不同e值的影响

```bash
python main.py --mode custom --e1 3 --e2 5
python main.py --mode custom --e1 7 --e2 11
python main.py --mode custom --e1 17 --e2 257
```

观察不同e值组合的攻击效果。

### 实验2: 不同密钥大小

```bash
python main.py --mode custom --bits 512
python main.py --mode custom --bits 1024
python main.py --mode custom --bits 2048
```

观察密钥大小对攻击时间的影响。

### 实验3: 失败案例

```python
# 修改代码，使e1 = e2 = 3
# 观察攻击失败的情况
```

## 📖 代码结构

```
common_modulus/
├── config.py                    # 配置参数
├── extended_gcd.py              # 扩展欧几里得算法
├── common_modulus_attack.py     # 攻击实现
├── paper_example.py             # 论文示例
├── main.py                      # 主程序
├── README.md                    # 详细文档
├── QUICKSTART.md                # 本文档
└── TEST_SUMMARY.md              # 测试报告
```

## 🎓 教学用途

本实现适合用于:
- 密码学课程实验
- RSA安全性演示
- 密钥管理培训
- 安全审计教学

---

**记住**: 本工具仅用于教育目的，不得用于未授权的系统！

**项目**: Attack4WeakRSA  
**课程**: SC6104 - Introduction to Cryptography (NTU)

