# Wiener Attack Usage Guide

Quick reference for using the Wiener Attack implementation.

---

## Quick Start

### 1. Run Complete Demonstration

Shows all features including success and failure cases:

```bash
python main.py demo
```

**What it shows**:
- Demo 1: Basic Wiener attack with very small d
- Demo 2: Boundary comparison across different N sizes
- Demo 3: All three methods succeed (d=122 bits)
- Demo 4: Demonstrating theoretical boundaries (d=128 bits, Wiener fails)

---

## Command Line Interface

### Attack Command

Run a single attack method:

```bash
# Wiener attack
python main.py attack --bits 512 --type wiener

# Bunder-Tonien attack
python main.py attack --bits 512 --type bunder_tonien

# New Boundary attack
python main.py attack --bits 512 --type new_boundary
```

**Parameters**:
- `--bits`: RSA modulus bit length (default: 512)
- `--type`: Attack method (wiener, bunder_tonien, new_boundary)

---

### Compare Command

Compare all three attack methods:

#### Option 1: All Methods Succeed

```bash
python main.py compare --bits 512 --d-ratio 0.24
```

**Result**:
```
d = 122 bits (< Wiener boundary 126 bits)

Wiener:         ✓ Success
Bunder-Tonien:  ✓ Success
New Boundary:   ✓ Success
```

#### Option 2: Demonstrate Theoretical Boundaries

```bash
python main.py compare --bits 512 --d-ratio 0.25
```

**Result**:
```
d = 128 bits (> Wiener boundary 126 bits)

Wiener:         ✗ Failed   ← d exceeds boundary
Bunder-Tonien:  ✓ Success  ← larger boundary
New Boundary:   ✓ Success  ← larger boundary
```

**Parameters**:
- `--bits`: RSA modulus bit length (default: 512)
- `--d-ratio`: d size ratio (default: 0.24)
  - `0.24`: All methods succeed (d ≈ 122 bits)
  - `0.25`: Demonstrates boundaries (d ≈ 128 bits)

---

## Understanding the Results

### Why Does Wiener Fail Sometimes?

This is **NOT a bug** - it's a demonstration of theoretical limits!

#### Three Attack Methods Have Different Boundaries:

| Method | Boundary Condition | For 512-bit N |
|--------|-------------------|---------------|
| **Wiener (1990)** | d < N^0.25 / 3 | ~126 bits |
| **Bunder-Tonien (2017)** | d < 2√(2N) | ~257 bits |
| **New Boundary (2023)** | d < √(8.24264N) | ~257 bits |

#### Example Scenarios:

**Scenario 1: d = 122 bits**
```
✓ Wiener:        122 < 126  → Success
✓ Bunder-Tonien: 122 < 257  → Success
✓ New Boundary:  122 < 257  → Success
```

**Scenario 2: d = 128 bits**
```
✗ Wiener:        128 > 126  → Failed (exceeds boundary)
✓ Bunder-Tonien: 128 < 257  → Success
✓ New Boundary:  128 < 257  → Success
```

**Scenario 3: d = 260 bits**
```
✗ Wiener:        260 > 126  → Failed
✗ Bunder-Tonien: 260 > 257  → Failed
✗ New Boundary:  260 > 257  → Failed
```

---

## Using as a Library

### Basic Usage

```python
from core import WienerAttack, BunderTonienAttack, NewBoundaryAttack

# Create attack instance
attack = WienerAttack()

# Execute attack
d = attack.attack(e, n)

if d:
    print(f"Recovered private key: {d}")
else:
    print("Attack failed")
```

### Generate Weak Keys for Testing

```python
from core import WeakRSAGenerator

generator = WeakRSAGenerator()

# Generate with specific d ratio
n, e, d, p, q = generator.generate_weak_rsa(bits=512, d_ratio=0.24)

# Check vulnerability
vuln_info = generator.check_vulnerability(n, d)
print(f"Wiener vulnerable: {vuln_info['wiener_vulnerable']}")
print(f"Bunder-Tonien vulnerable: {vuln_info['bunder_tonien_vulnerable']}")
```

### Run Comparison

```python
from runner import run_comparison

# Generate weak key
n, e, d, p, q = generator.generate_weak_rsa(bits=512, d_ratio=0.24)

# Compare all methods
results = run_comparison(n, e, d)

# Check results
for method, result in results.items():
    print(f"{method}: {'Success' if result['success'] else 'Failed'}")
```

---

## Running Tests

```bash
# Run all unit tests
cd tests
python test_wiener.py
```

**Expected output**:
```
======================================================================
Running Wiener Attack Tests
======================================================================

[Test 1] Basic Wiener Attack                    ✓
[Test 2] Bunder-Tonien Attack                   ✓
[Test 3] New Boundary Attack                    ✓
[Test 4] Boundary Comparison                    ✓
[Test 5] Weak Key Generation                    ✓
[Test 6] Vulnerability Check                    ✓
[Test 7] Encryption/Decryption Verification     ✓

======================================================================
Test Results: 7 passed, 0 failed
======================================================================
```

---

## Theoretical Background

### Original Wiener Attack (1990)

**Condition**: d < N^0.25 / 3

**Principle**: 
- Uses continued fraction expansion of e/N
- Finds convergents k/d where k/d ≈ e/N
- Works when d is very small

**Complexity**: O(log N)

### Bunder-Tonien Attack (2017)

**Condition**: d < 2√(2N)

**Improvement**:
- Relaxed Wiener's boundary condition
- Uses modified N' = floor(N - (1 + 3/(2√2))√N + 1)
- Can attack larger d values

**Enhancement**: ~N^0.25 times larger boundary than Wiener

### New Boundary Attack (2023)

**Condition**: d < √(8.24264N)

**Improvement**:
- Further relaxed boundary
- Derived through derivative and limit analysis
- α = 8 + 6√2 ≈ 16.4853

**Enhancement**: ~1.01x larger boundary than Bunder-Tonien

---

## Key Insights

### 1. Theoretical Limits Matter

The failure of Wiener attack when d=128 bits demonstrates:
- Each attack method has a **theoretical boundary**
- Attacks **cannot succeed** beyond their boundary
- This is **fundamental mathematics**, not a code bug

### 2. Progressive Improvements

The three methods show the evolution of research:
- **1990**: Original Wiener attack
- **2017**: Bunder-Tonien relaxed the boundary
- **2023**: New Boundary further improved it

### 3. Practical Implications

For RSA security:
- **Avoid**: d < √(8.24264N) (vulnerable to all three)
- **Safe**: d > N^0.5 (standard RSA)
- **Recommended**: Use standard key generation (e=65537, random d)

---

## Troubleshooting

### Q: Why does Wiener attack fail?

**A**: Check if d exceeds the boundary:
```
d bit length: 128
Wiener boundary: 126 bits
128 > 126 → Attack fails (expected behavior)
```

### Q: How to make all attacks succeed?

**A**: Use smaller d:
```bash
python main.py compare --d-ratio 0.24  # d ≈ 122 bits
```

### Q: How to demonstrate boundaries?

**A**: Use medium d:
```bash
python main.py compare --d-ratio 0.25  # d ≈ 128 bits
```

---

## References

1. **Wiener, M. (1990)**: "Cryptanalysis of Short RSA Secret Exponents"
2. **Bunder & Tonien (2017)**: "A New Attack on the RSA Cryptosystem Based on Continued Fractions"
3. **New Boundary (2023)**: "A New Boundary of Minimum Private Key on Wiener Attack Against RSA Algorithm"

---

## Support

For issues or questions:
- Check `README.md` for detailed documentation
- See `REFACTORING_SUMMARY.md` for architecture details
- Run `python main.py --help` for CLI help

