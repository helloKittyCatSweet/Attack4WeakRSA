#!/usr/bin/env python3
"""
Main demonstration program for Fermat factorization of RSA with close primes
"""

import argparse
import sys
import time
from primality import PrimalityTester
from prime_generator import ClosePrimeGenerator
from fermat_factorizer import FermatFactorizer
from rsa_demo import RSADemo
from utils import human_readable_int, format_timing_statistics, print_timing_stats, validate_parameters
from config import DEFAULT_CONFIG, SAFE_PARAMETERS


class FermatAttackDemo:
    """Main demonstration orchestrator"""

    def __init__(self):
        self.prime_gen = ClosePrimeGenerator()
        self.factorizer = FermatFactorizer()
        self.rsa_demo = RSADemo()
        self.primality_tester = PrimalityTester()

    def run_fermat_demo(self, bits, max_gap, rounds):
        """Run Fermat factorization timing demonstration"""
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
            timings = self.factorizer.run_multiple_trials(self.prime_gen, bits, max_gap, rounds)
            stats = format_timing_statistics(timings)
            print_timing_stats(stats)

    def run_rsa_demo(self, bits, max_gap, message):
        """Run complete RSA encryption/decryption demonstration"""
        print(f"Generating RSA keypair with close primes (~{bits} bits each)...")

        # Generate RSA keypair
        n, e, d, p, q = self.rsa_demo.generate_rsa_keypair(bits, max_gap)
        print(f"n bits = {n.bit_length()}  e = {e}")

        # Encrypt message
        ciphertext = self.rsa_demo.encrypt_message(message, n, e)
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
        d_recovered = self.rsa_demo._modular_inverse(e, phi)
        decrypted_text = self.rsa_demo.decrypt_message(ciphertext, n, d_recovered)

        print(f"Decrypted text: {decrypted_text}")
        print(f"Original text:  {message}")
        print(f"Match: {decrypted_text == message}")


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Demonstrate Fermat factorization on RSA with close primes"
    )
    parser.add_argument("--bits", type=int, default=DEFAULT_CONFIG['bits'],
                        help="Bit-length of primes to generate")
    parser.add_argument("--max-gap", type=int, default=DEFAULT_CONFIG['max_gap'],
                        help="Maximum distance between primes")
    parser.add_argument("--rounds", type=int, default=DEFAULT_CONFIG['rounds'],
                        help="Number of trials for timing")
    parser.add_argument("--mode", choices=['fermat', 'rsa'],
                        default=DEFAULT_CONFIG['mode'],
                        help="Demo mode: fermat or rsa")
    parser.add_argument("--message", type=str, default=DEFAULT_CONFIG['message'],
                        help="Plaintext for RSA demo")
    return parser.parse_args()


def main():
    """Main program entry point"""
    args = parse_arguments()

    # Validate parameters
    if not validate_parameters(args.bits, args.max_gap, SAFE_PARAMETERS):
        return 1

    # Warn about large parameters
    if args.bits >= 100 and args.max_gap > (1 << 18):
        print("Warning: Large parameters may take significant time")

    # Run demonstration
    demo = FermatAttackDemo()

    try:
        if args.mode == 'fermat':
            demo.run_fermat_demo(args.bits, args.max_gap, args.rounds)
        else:
            demo.run_rsa_demo(args.bits, args.max_gap, args.message)
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        return 1
    except Exception as e:
        print(f"Error during demonstration: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())