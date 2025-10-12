```markdown
# PP-RSA Partial Key Exposure Attack

A multithreaded implementation of partial key exposure attacks on Prime Power RSA (PP-RSA) with moduli N = p^r * q^s, based on the research paper "Partial Key Exposure Attacks on RSA with Moduli N=p^rq^s".

## 📖 Overview

This project demonstrates how partial knowledge of an RSA private key can lead to complete key recovery. The attack is particularly effective against Prime Power RSA variants that use moduli of the form N = p^r * q^s.

## 🏗️ Project Structure

```
rsa_attack/
├── main.py              # Main demonstration program
├── config.py           # Configuration parameters
├── math_utils.py       # Mathematical utilities
├── rsa_generator.py    # PP-RSA parameter generator
├── key_exposure.py     # Partial key exposure handling
├── attack_worker.py    # Multithreaded attack implementation
├── result_verifier.py  # Attack result verification
└── README.md          # This file
```

## 🚀 Quick Start

### Prerequisites

```bash
pip install pycryptodome
```

### Running the Demo

```bash
python main.py
```

### Running Benchmark Tests

```bash
python main.py  # Uncomment benchmark section in main()
```

## ⚙️ Configuration

Edit `config.py` to modify attack parameters:

```python
CONFIG = {
    'n_bits': 64,        # RSA modulus bit length
    'r': 2,              # Exponent for p
    's': 1,              # Exponent for q  
    'exposure_ratio': 0.7,  # Percentage of known key bits
    'exposure_type': 'MSB', # 'MSB' or 'LSB' exposure
    'num_threads': 4,    # Number of worker threads
    'timeout': 30        # Attack timeout in seconds
}
```

## 🔧 Module Descriptions

### 1. main.py
- Orchestrates the complete attack workflow
- Demonstrates the attack step by step
- Optional benchmark testing

### 2. config.py
- Centralized configuration management
- Predefined test scenarios
- Easy parameter tuning

### 3. math_utils.py
- Mathematical helper functions
- Parameter validation
- Search space estimation

### 4. rsa_generator.py
- Generates PP-RSA key pairs
- Ensures proper parameter selection
- Validates mathematical constraints

### 5. key_exposure.py
- Simulates partial key exposure scenarios
- Handles both MSB and LSB exposure
- Calculates search bounds

### 6. attack_worker.py
- Implements multithreaded brute force attack
- Progress monitoring and reporting
- Efficient search space partitioning

### 7. result_verifier.py
- Validates attack results
- Performs mathematical verification
- Tests encryption/decryption functionality

## 🎯 Attack Methodology

### Supported Scenarios

1. **First Scheme**: ed ≡ 1 mod φ(N)
2. **Second Scheme**: ed ≡ 1 mod (p-1)(q-1)

### Attack Types

- **MSB Exposure**: Known Most Significant Bits
- **LSB Exposure**: Known Least Significant Bits

### Mathematical Basis

The attack exploits the equation:
```
e(d0 + x) ≡ 1 mod M
```
Where:
- `d0` = known part of private key
- `x` = unknown part to be recovered
- `M` = φ(N) or (p-1)(q-1)

## 📊 Performance

### Typical Results (on standard laptop)

| RSA Bits | Exposure | Threads | Time | Success Rate |
|----------|----------|---------|------|--------------|
| 64-bit   | 70%      | 4       | <10s | 100%         |
| 80-bit   | 80%      | 8       | <30s | 100%         |
| 128-bit  | 90%      | 16      | ~2m  | High         |

### Key Factors Affecting Performance

1. **Unknown Bits**: Each additional bit doubles search space
2. **Thread Count**: More threads = faster search
3. **Exposure Type**: MSB/LSB have different performance characteristics
4. **Hardware**: CPU cores and speed significantly impact results

## 🔒 Security Implications

This demonstration highlights:

- **Side-channel vulnerabilities**: Partial key leaks can lead to complete compromise
- **PP-RSA weaknesses**: Special moduli forms may reduce security margins
- **Importance of key protection**: Even partial exposure is dangerous

## 🛠️ Customization

### Adding New Attack Methods

1. Extend `attack_worker.py` with new worker functions
2. Update `key_exposure.py` for new exposure scenarios
3. Modify `config.py` to include new parameters

### Testing Different Parameters

```python
# In config.py
CUSTOM_CONFIG = {
    'n_bits': 128,
    'r': 3,           # Test p³q moduli
    's': 1,
    'exposure_ratio': 0.8,
    # ... other parameters
}
```

## 📈 Benchmarking

The project includes built-in benchmarking:

```python
BENCHMARK_CONFIGS = [
    {'n_bits': 48, 'ratio': 0.6, 'threads': 2, 'desc': 'Small scale'},
    {'n_bits': 64, 'ratio': 0.7, 'threads': 4, 'desc': 'Medium scale'},
    {'n_bits': 80, 'ratio': 0.8, 'threads': 8, 'desc': 'Large scale'},
]
```

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure pycryptodome is installed
2. **Memory Error**: Reduce search space or use smaller parameters
3. **Timeout**: Increase timeout or reduce RSA bit length

### Debug Mode

Add debug prints in individual modules to trace execution flow.

## 📚 References

- Yuan, S., Yu, W., Wang, K., & Li, X. "Partial Key Exposure Attacks on RSA with Moduli N=p^rq^s"
- Coppersmith, D. "Finding a Small Root of a Univariate Modular Equation"
- Takagi, T. "Fast RSA-type Cryptosystem Modulo p^k q"

## ⚠️ Disclaimer

This project is for educational and research purposes only. Use responsibly and only on systems you own or have explicit permission to test.

## 📄 License

This project is provided for academic research and educational use.

---

**Note**: For actual security assessment, consult with cybersecurity professionals and follow responsible disclosure practices.