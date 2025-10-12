# Fermat Factorization RSA Attack

A demonstration of Fermat's factorization method against RSA moduli with close prime factors.

## 📖 Overview

This project demonstrates how RSA becomes vulnerable when the two prime factors `p` and `q` are close together. Fermat's factorization method can efficiently factor such moduli, breaking the RSA encryption.

## 🎯 Key Features

- **Miller-Rabin primality testing** for prime generation
- **Close prime pair generation** for vulnerable RSA keys
- **Fermat factorization** implementation
- **Complete RSA demo** with encryption → factorization → decryption
- **Performance benchmarking** with timing statistics
- **Modular architecture** for easy extension

## 🏗️ Project Structure

```
fermat_rsa_attack/
├── main.py              # Main demonstration program
├── config.py           # Configuration parameters
├── primality.py        # Miller-Rabin primality testing
├── prime_generator.py  # Close prime pair generation
├── fermat_factorizer.py # Fermat factorization algorithm
├── rsa_demo.py         # RSA encryption/decryption demo
├── utils.py            # Utility functions
└── README.md          # This file
```

## 🚀 Quick Start

### Basic Fermat Factorization Demo

```bash
python main.py --bits 60 --max-gap 16384 --mode fermat
```

### Complete RSA Demo

```bash
python main.py --bits 60 --max-gap 16384 --mode rsa --message "Hello RSA"
```

### Multiple Trials for Timing

```bash
python main.py --bits 60 --max-gap 16384 --rounds 5 --mode fermat
```

## ⚙️ Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--bits` | 60 | Bit length of RSA primes |
| `--max-gap` | 16384 | Maximum distance between primes |
| `--rounds` | 1 | Number of timing trials |
| `--mode` | fermat | Demo mode: `fermat` or `rsa` |
| `--message` | "NTU demo" | Plaintext for RSA demo |

## 🔧 Module Descriptions

### 1. primality.py
- **Miller-Rabin probabilistic primality test**
- Efficient prime verification
- Next prime finding algorithm

### 2. prime_generator.py
- Generate close prime pairs
- Control prime distance with `max-gap`
- Ensure proper bit lengths

### 3. fermat_factorizer.py
- Implement Fermat's factorization method
- Performance timing and benchmarking
- Multiple trial support

### 4. rsa_demo.py
- Complete RSA key generation
- Encryption and decryption
- Modular arithmetic utilities

### 5. utils.py
- Number formatting
- Timing statistics
- Parameter validation

## 🎪 Demonstration Modes

### Fermat Factorization Mode
- Generates close primes
- Computes RSA modulus n = p × q
- Times the factorization process
- Provides performance statistics

### RSA End-to-End Mode
1. Generates vulnerable RSA keypair
2. Encrypts a message
3. Factors the modulus using Fermat
4. Recovers private key
5. Decrypts the message

## 📊 Performance Characteristics

### Factorization Time vs Prime Gap
| Prime Gap | Steps | Time (60-bit primes) |
|-----------|--------|---------------------|
| 1,000     | ~500   | <1 ms              |
| 10,000    | ~5,000 | ~5 ms              |
| 100,000   | ~50,000| ~50 ms             |

### Recommended Parameters
- **Educational**: 40-80 bits, gap < 10,000
- **Demonstration**: 60-100 bits, gap < 50,000  
- **Research**: 100-128 bits, gap < 100,000

## 🧮 Mathematical Background

### Fermat's Factorization
For n = p × q where p and q are close:
1. Start from a = ⌈√n⌉
2. Check if a² - n is a perfect square
3. If b² = a² - n, then p = a - b, q = a + b
4. Increment a until solution found

### Complexity
- **Worst case**: O(n) when primes are far apart
- **Best case**: O(1) when primes are very close
- **Typical**: O(√(p-q)) for close primes

## ⚠️ Security Implications

This demonstration shows:
- **RSA security requires random prime selection**
- **Close primes make factorization trivial**
- **Proper prime generation is critical**
- **Fermat's method is practical for close primes**

## 🔬 Academic Context

Based on the observation that:
- RSA moduli with |p-q| < 2^(k/4) are vulnerable
- Fermat's method becomes efficient for close primes
- Real-world implementations must avoid this pitfall

## 🛠️ Extension Ideas

1. **Add more factorization methods** (Pollard's rho, p-1)
2. **Implement Coppersmith's method** for partial key exposure
3. **Add graphical timing plots**
4. **Support for larger bit lengths** with optimization
5. **Network demo** with client-server factorization

## 📚 References

- Fermat's factorization method (1643)
- "Handbook of Applied Cryptography" - Menezes, van Oorschot, Vanstone
- RSA Security Standards

## ⚠️ Disclaimer

This project is for **educational purposes only**. Use only on systems you own or have explicit permission to test.

## 🐛 Troubleshooting

### Common Issues

1. **Long execution time**: Reduce `--bits` or `--max-gap`
2. **Memory error**: Use smaller parameters
3. **Factorization fails**: Increase `--max-gap` or check primality

### Performance Tips

- Use 40-80 bits for quick demonstrations
- Keep max-gap under 100,000 for reasonable times
- Start with fermat mode before full RSA demo

---

**Note**: This demonstrates a specific vulnerability. Real RSA implementations use proper prime spacing.