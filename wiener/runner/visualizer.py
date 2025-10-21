"""
Visualization tools for Wiener attack analysis

Handles all printing and formatting.
"""

import math
from typing import Dict, Any


def print_header(title: str):
    """Print header"""
    width = 70
    print("\n" + "="*width)
    print(title.center(width))
    print("="*width)


def print_section(title: str):
    """Print section title"""
    print(f"\n[{title}]")
    print("-"*70)


def print_key_info(n: int, e: int, d: int, p: int = None, q: int = None):
    """Print key information"""
    print(f"  N = {n}")
    print(f"  e = {e}")
    print(f"  d = {d}")
    if p and q:
        print(f"  p = {p}")
        print(f"  q = {q}")
    print(f"\n  Bit lengths:")
    print(f"    N: {n.bit_length()} bits")
    print(f"    e: {e.bit_length()} bits")
    print(f"    d: {d.bit_length()} bits")
    if p and q:
        print(f"    p: {p.bit_length()} bits")
        print(f"    q: {q.bit_length()} bits")


def print_boundary_comparison(n: int, d: int):
    """Print boundary comparison"""
    wiener_bound = n ** 0.25 / 3
    bt_bound = 2 * math.sqrt(2 * n)
    new_bound = math.sqrt(8.24264 * n)
    
    print(f"\n  Private key d = {d}")
    print(f"  d bit length: {d.bit_length()}")
    print(f"\n  {'Attack Method':<20} {'Boundary':<20} {'d < Boundary':<15} {'Bits':<10}")
    print("  " + "-"*70)
    
    print(f"  {'Wiener (1990)':<20} {wiener_bound:<20.2e} {str(d < wiener_bound):<15} {int(math.log2(wiener_bound)) if wiener_bound > 0 else 0:<10}")
    print(f"  {'Bunder-Tonien':<20} {bt_bound:<20.2e} {str(d < bt_bound):<15} {int(math.log2(bt_bound)) if bt_bound > 0 else 0:<10}")
    print(f"  {'New Boundary':<20} {new_bound:<20.2e} {str(d < new_bound):<15} {int(math.log2(new_bound)) if new_bound > 0 else 0:<10}")


def print_attack_result(method: str, success: bool, d_original: int = None, d_recovered: int = None, time_ms: float = 0):
    """Print attack result"""
    print(f"\n  Attack method: {method}")
    print(f"  Result: {'✓ Success' if success else '✗ Failed'}")
    if success and d_original and d_recovered:
        print(f"  Original d: {d_original}")
        print(f"  Recovered d: {d_recovered}")
        print(f"  Match: {'✓' if d_original == d_recovered else '✗'}")
    print(f"  Time: {time_ms:.3f} ms")


def print_comparison_table(results: Dict[str, Any]):
    """Print comparison table"""
    print(f"\n  {'Method':<20} {'Success':<10} {'Time(ms)':<15} {'Time(s)':<15}")
    print("  " + "-"*65)
    
    for method, result in results.items():
        success = '✓' if result['success'] else '✗'
        time_ms = result['time'] * 1000
        time_s = result['time']
        print(f"  {method:<20} {success:<10} {time_ms:<15.3f} {time_s:<15.6f}")


def print_benchmark_table(results: list):
    """Print benchmark table"""
    print(f"\n  {'RSA Bits':<15} {'Time(s)':<15} {'Time(ms)':<15} {'Status':<10}")
    print("  " + "-"*60)
    
    for r in results:
        status = '✓' if r['success'] else '✗'
        print(f"  {r['bits']:<15} {r['time']:<15.3f} {r['time']*1000:<15.2f} {status:<10}")


def print_boundary_test_table(results: list):
    """Print boundary test table"""
    print(f"\n  {'d Ratio':<10} {'Wiener':<15} {'Bunder-Tonien':<20} {'New Boundary':<15}")
    print("  " + "-"*65)
    
    for r in results:
        print(f"  {r['ratio']:<10.2f} {r['wiener']*100:<14.0f}% {r['bunder_tonien']*100:<19.0f}% {r['new_boundary']*100:<14.0f}%")


def print_ascii_chart(data: Dict[str, float], title: str = "Chart", max_width: int = 50):
    """Print ASCII chart"""
    print(f"\n  {title}")
    print("  " + "-"*max_width)
    
    if not data:
        return
    
    max_val = max(data.values())
    
    for label, value in data.items():
        bar_length = int((value / max_val) * max_width) if max_val > 0 else 0
        bar = "█" * bar_length
        print(f"  {label:<15} {bar} {value:.2e}")


def print_theoretical_analysis():
    """Print theoretical analysis"""
    print_header("Theoretical Analysis")
    
    print("\n1. Wiener Attack (1990)")
    print("   Condition: d < N^0.25 / 3")
    print("   Principle: Continued fraction expansion e/N ≈ k/d")
    print("   Complexity: O(log N)")
    
    print("\n2. Bunder-Tonien Attack (2017)")
    print("   Condition: d < 2√(2N)")
    print("   Improvement: Relaxed Wiener's boundary")
    print("   Enhancement: ~N^0.25 times")
    
    print("\n3. New Boundary Attack (2023)")
    print("   Condition: d < √(8.24264N)")
    print("   Derivation: Through derivative and limit analysis")
    print("   Formula: α = 8 + 6√2 ≈ 16.4853")
    print("            d < (α/2)√N")
    print("   Enhancement: ~1.01x vs Bunder-Tonien")
    
    print("\n Key Inequality (Lemma 3.1):")
    print("   (3√2 - 2N + 4) / (2N - 3√(2N)) < 1/(αN)")
    print("   When N → ∞, left side → 1/(8 + 6√2)")


def print_security_recommendations():
    """Print security recommendations"""
    print_header("Security Recommendations")
    
    print("\n✓ Recommended Practices:")
    print("  1. Use standard RSA key generation algorithms")
    print("  2. Ensure d > N^0.5")
    print("  3. RSA modulus ≥ 2048 bits")
    print("  4. Public exponent e = 65537")
    print("  5. Follow NIST SP 800-56B standard")
    
    print("\n✗ Avoid:")
    print("  1. Don't manually choose small private key d")
    print("  2. Don't use too small RSA modulus")
    print("  3. Don't sacrifice security for performance")
    print("  4. Don't reuse keypairs")
    
    print("\n⚠ Vulnerability Detection:")
    print("  If d < √(8.24264N), vulnerable to new boundary attack")
    print("  If d < 2√(2N), vulnerable to Bunder-Tonien attack")
    print("  If d < N^0.25/3, vulnerable to Wiener attack")


def print_complexity_analysis():
    """Print complexity analysis"""
    print_header("Complexity Analysis")
    
    print("\nTime Complexity: O(log N)")
    print("\nMain Steps:")
    print("  1. Continued fraction expansion (Euclidean algorithm): O(log N)")
    print("  2. Convergent computation: O(log N)")
    print("  3. Candidate verification: O(log N) times, each O(1)")
    print("\nSpace Complexity: O(log N)")
    print("  Store continued fraction convergents")
    
    print("\nActual Performance:")
    print("  512-bit RSA:  ~0.02s")
    print("  1024-bit RSA: ~0.05s")
    print("  2048-bit RSA: ~0.15s")
    print("  4096-bit RSA: ~0.75s")
    print("  8192-bit RSA: ~4.5s")
    
    print("\nVs Brute Force:")
    print("  Brute force: O(2^(d bit length))")
    print("  Wiener attack: O(log N)")
    print("  Efficiency gain: Exponential")


class ProgressBar:
    """Progress bar"""
    
    def __init__(self, total: int, width: int = 50, prefix: str = "Progress"):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.current = 0
    
    def update(self, current: int):
        """Update progress"""
        self.current = current
        percent = (current / self.total) * 100
        filled = int((current / self.total) * self.width)
        bar = "█" * filled + "-" * (self.width - filled)
        print(f"\r  {self.prefix}: |{bar}| {percent:.1f}% ({current}/{self.total})", end="", flush=True)
    
    def finish(self):
        """Finish"""
        self.update(self.total)
        print()

