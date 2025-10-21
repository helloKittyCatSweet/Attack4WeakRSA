#!/usr/bin/env python3
"""
Main CLI entry point for Fermat factorization RSA attack demonstration

Usage:
    python main_new.py fermat --bits 60 --max-gap 16384 --rounds 5
    python main_new.py rsa --bits 60 --max-gap 16384 --message "Hello"
"""

import argparse
import sys

# Handle both direct execution and module execution
try:
    from runner import DemoConfig, run_fermat_demo, run_rsa_demo, DEFAULT_CONFIG
except ImportError:
    from .runner import DemoConfig, run_fermat_demo, run_rsa_demo, DEFAULT_CONFIG


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser with subcommands"""
    parser = argparse.ArgumentParser(
        description="Fermat Factorization Attack on RSA with Close Primes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run Fermat factorization demo
  python main_new.py fermat --bits 60 --max-gap 16384

  # Run RSA attack demo
  python main_new.py rsa --bits 60 --message "NTU demo"

  # Multiple timing rounds
  python main_new.py fermat --bits 80 --rounds 10
        """
    )

    # Create subparsers for different modes
    subparsers = parser.add_subparsers(dest='mode', help='Demo mode', required=True)

    # Fermat factorization subcommand
    fermat_parser = subparsers.add_parser(
        'fermat',
        help='Run Fermat factorization timing demo'
    )
    fermat_parser.add_argument(
        '--bits', type=int, default=DEFAULT_CONFIG.bits,
        help=f'Bit-length of primes (default: {DEFAULT_CONFIG.bits})'
    )
    fermat_parser.add_argument(
        '--max-gap', type=int, default=DEFAULT_CONFIG.max_gap,
        help=f'Maximum distance between primes (default: {DEFAULT_CONFIG.max_gap})'
    )
    fermat_parser.add_argument(
        '--rounds', type=int, default=DEFAULT_CONFIG.rounds,
        help=f'Number of timing trials (default: {DEFAULT_CONFIG.rounds})'
    )

    # RSA attack subcommand
    rsa_parser = subparsers.add_parser(
        'rsa',
        help='Run complete RSA encryption/decryption attack demo'
    )
    rsa_parser.add_argument(
        '--bits', type=int, default=DEFAULT_CONFIG.bits,
        help=f'Bit-length of primes (default: {DEFAULT_CONFIG.bits})'
    )
    rsa_parser.add_argument(
        '--max-gap', type=int, default=DEFAULT_CONFIG.max_gap,
        help=f'Maximum distance between primes (default: {DEFAULT_CONFIG.max_gap})'
    )
    rsa_parser.add_argument(
        '--message', type=str, default=DEFAULT_CONFIG.message,
        help=f'Plaintext message (default: "{DEFAULT_CONFIG.message}")'
    )
    rsa_parser.add_argument(
        '--public-exponent', '-e', type=int, default=DEFAULT_CONFIG.public_exponent,
        help=f'RSA public exponent (default: {DEFAULT_CONFIG.public_exponent})'
    )

    return parser


def main() -> int:
    """
    Main program entry point.

    Returns:
        Exit code (0 = success, 1 = error)
    """
    parser = create_parser()
    args = parser.parse_args()

    # Create configuration from arguments
    config = DemoConfig(
        bits=args.bits,
        max_gap=args.max_gap,
        rounds=getattr(args, 'rounds', 1),
        mode=args.mode,
        message=getattr(args, 'message', DEFAULT_CONFIG.message),
        public_exponent=getattr(args, 'public_exponent', DEFAULT_CONFIG.public_exponent)
    )

    # Display configuration
    print("="*70)
    print(f"Fermat Factorization RSA Attack - {config.mode.upper()} Mode")
    print("="*70)
    print(f"Configuration:")
    print(f"  Bits:       {config.bits}")
    print(f"  Max Gap:    {config.max_gap}")
    if config.mode == 'fermat':
        print(f"  Rounds:     {config.rounds}")
    else:
        print(f"  Message:    {config.message}")
        print(f"  Exponent:   {config.public_exponent}")
    print("="*70)
    print()

    # Run appropriate demo
    if config.mode == 'fermat':
        return run_fermat_demo(config)
    else:
        return run_rsa_demo(config)


if __name__ == "__main__":
    sys.exit(main())

