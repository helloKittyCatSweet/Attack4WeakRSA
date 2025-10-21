"""
Demo runners for Fermat factorization and RSA attack
"""

import sys
from typing import List

# Handle both direct and module execution
try:
    from core import FermatFactorizer, ClosePrimeGenerator, RSAKeyGenerator, RSAEncryptor
    from core.rsa import modular_inverse, bytes_to_int, int_to_bytes
    from utils import human_readable_int, format_timing_statistics, print_timing_stats
    from utils import validate_parameters, ValidationResult
    from runner.config import DemoConfig, SAFE_PARAMETERS
except ImportError:
    from ..core import FermatFactorizer, ClosePrimeGenerator, RSAKeyGenerator, RSAEncryptor
    from ..core.rsa import modular_inverse, bytes_to_int, int_to_bytes
    from ..utils import human_readable_int, format_timing_statistics, print_timing_stats
    from ..utils import validate_parameters, ValidationResult
    from .config import DemoConfig, SAFE_PARAMETERS


class FermatDemo:
    """Fermat factorization timing demonstration"""

    def __init__(self):
        self.prime_gen = ClosePrimeGenerator()
        self.factorizer = FermatFactorizer()

    def run(self, bits: int, max_gap: int, rounds: int = 1) -> None:
        """
        Run Fermat factorization timing demonstration.

        Args:
            bits: Bit length for primes
            max_gap: Maximum gap between primes
            rounds: Number of timing rounds
        """
        print(f"Generating ~{bits}-bit close primes with max_gap={max_gap}...")

        # Generate and display primes
        p, q = self.prime_gen.generate_close_primes(bits, max_gap)
        gap = self.prime_gen.calculate_prime_gap(p, q)
        n = p * q

        print(f"p bit_length={p.bit_length()}  q bit_length={q.bit_length()}")
        print(f"p = {human_readable_int(p)}")
        print(f"q = {human_readable_int(q)}")
        print(f"|q-p| = {gap}  (estimated Fermat steps ≈ {gap // 2})")
        print(f"n = p*q has {n.bit_length()} bits")

        # Factor via Fermat
        print("\nFactoring n with Fermat factorization...")
        result, elapsed_ms = self.factorizer.factor_with_timing(n)

        if result is None:
            print("Fermat factorization failed (unexpected in this demo)")
            return

        rp, rq = result
        success = (rp == p and rq == q) or (rp == q and rq == p)
        print(f"Recovered p, q correctly: {success}")
        print(f"Time: {elapsed_ms:.3f} ms")

        # Multiple trials for timing statistics
        if rounds > 1:
            print(f"\nRunning {rounds} trials for timing analysis...")
            timings = self._run_multiple_trials(bits, max_gap, rounds)
            stats = format_timing_statistics(timings)
            print_timing_stats(stats)

    def _run_multiple_trials(self, bits: int, max_gap: int, rounds: int) -> List[float]:
        """Run multiple factorization trials and collect timings"""
        timings = []
        for _ in range(rounds):
            p, q = self.prime_gen.generate_close_primes(bits, max_gap)
            n = p * q
            _, elapsed_ms = self.factorizer.factor_with_timing(n)
            timings.append(elapsed_ms)
        return timings


class RSADemo:
    """Complete RSA encryption/decryption demonstration with Fermat attack"""

    def __init__(self):
        self.prime_gen = ClosePrimeGenerator()
        self.factorizer = FermatFactorizer()
        self.key_gen = RSAKeyGenerator()
        self.encryptor = RSAEncryptor()

    def run(self, bits: int, max_gap: int, message: str) -> None:
        """
        Run complete RSA encryption/decryption demonstration.

        Args:
            bits: Bit length for primes
            max_gap: Maximum gap between primes
            message: Plaintext message to encrypt
        """
        print(f"Generating RSA keypair with close primes (~{bits} bits each)...")

        # Generate RSA keypair
        n, e, d, p, q = self.key_gen.generate_keypair(bits, max_gap)
        print(f"n bits = {n.bit_length()}  e = {e}")

        # Encrypt message
        message_bytes = message.encode('utf-8')
        ciphertext = self.encryptor.encrypt_bytes(message_bytes, e, n)
        print(f"Ciphertext = {ciphertext}")

        # Factor modulus and recover private key
        print("\nAttacker factors n with Fermat factorization...")
        result, elapsed_ms = self.factorizer.factor_with_timing(n)

        if result is None:
            print("Factorization failed!")
            return

        fp, fq = result
        gap = abs(fp - fq)
        print(f"Recovered p and q in {elapsed_ms:.3f} ms; |q-p| = {gap}")

        # Recompute private key and decrypt
        phi = (fp - 1) * (fq - 1)
        d_recovered = modular_inverse(e, phi)
        decrypted_bytes = self.encryptor.decrypt_bytes(ciphertext, d_recovered, n)
        decrypted_text = decrypted_bytes.decode('utf-8')

        print(f"Decrypted text: {decrypted_text}")
        print(f"Original text:  {message}")
        print(f"Match: {decrypted_text == message}")


def run_fermat_demo(config: DemoConfig) -> int:
    """
    Run Fermat factorization demo with configuration.

    Args:
        config: Demo configuration

    Returns:
        Exit code (0 = success, 1 = error)
    """
    # Validate parameters
    result = validate_parameters(config.bits, config.max_gap, SAFE_PARAMETERS.__dict__)
    
    if not result.valid:
        print("Parameter validation failed:")
        for error in result.errors:
            print(f"  ERROR: {error}")
        return 1
    
    if result.has_warnings():
        for warning in result.warnings:
            print(f"  WARNING: {warning}")

    # Run demo
    try:
        demo = FermatDemo()
        demo.run(config.bits, config.max_gap, config.rounds)
        return 0
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        return 1
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_rsa_demo(config: DemoConfig) -> int:
    """
    Run RSA attack demo with configuration.

    Args:
        config: Demo configuration

    Returns:
        Exit code (0 = success, 1 = error)
    """
    # Validate parameters
    result = validate_parameters(config.bits, config.max_gap, SAFE_PARAMETERS.__dict__)
    
    if not result.valid:
        print("Parameter validation failed:")
        for error in result.errors:
            print(f"  ERROR: {error}")
        return 1
    
    if result.has_warnings():
        for warning in result.warnings:
            print(f"  WARNING: {warning}")

    # Run demo
    try:
        demo = RSADemo()
        demo.run(config.bits, config.max_gap, config.message)
        return 0
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        return 1
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1

