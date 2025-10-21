#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main CLI entry point for RSA Partial Key Exposure Attack

Provides command-line interface with subcommands for different operations.
"""

import argparse
import sys

# Handle both direct and module execution
try:
    from demo import run_single_attack, run_demonstration, run_benchmark, BenchmarkConfig
    from config import RSAConfig, ExperimentConfig
except ImportError:
    from .demo import run_single_attack, run_demonstration, run_benchmark, BenchmarkConfig
    from .config import RSAConfig, ExperimentConfig


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="RSA Partial Key Exposure Attack",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run demonstration
  python main.py demo
  
  # Run single attack
  python main.py attack --bits 20 --delta 0.7 --type MSB
  
  # Run benchmark
  python main.py benchmark --trials 10
  
  # Verbose mode
  python main.py demo --verbose
  
  # Quiet mode
  python main.py demo --quiet
        """
    )
    

    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration')
    
    # Attack command
    attack_parser = subparsers.add_parser('attack', help='Run single attack')
    attack_parser.add_argument('--bits', type=int, default=20,
                                help='Bit length of primes (default: 20)')
    attack_parser.add_argument('--r', type=int, default=2,
                                help='Exponent of p in N=p^r*q^s (default: 2)')
    attack_parser.add_argument('--s', type=int, default=1,
                                help='Exponent of q in N=p^r*q^s (default: 1)')
    attack_parser.add_argument('--delta', type=float, default=0.7,
                                help='Fraction of known bits (default: 0.7)')
    attack_parser.add_argument('--type', type=str, default='MSB', choices=['MSB', 'LSB'],
                                help='Exposure type (default: MSB)')
    attack_parser.add_argument('--m', type=int, default=None,
                                help='Lattice parameter m (auto if not specified)')
    attack_parser.add_argument('--t', type=int, default=None,
                                help='Lattice parameter t (auto if not specified)')
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser('benchmark', help='Run benchmark')
    benchmark_parser.add_argument('--trials', type=int, default=5,
                                   help='Number of trials per configuration (default: 5)')
    benchmark_parser.add_argument('--bits', type=int, nargs='+', default=[16, 18, 20],
                                   help='Bit lengths to test (default: 16 18 20)')
    benchmark_parser.add_argument('--deltas', type=float, nargs='+', default=[0.6, 0.7, 0.8],
                                   help='Deltas to test (default: 0.6 0.7 0.8)')
    
    args = parser.parse_args()

    # Execute command
    if args.command == 'demo':
        run_demonstration()
    
    elif args.command == 'attack':
        # Setup configurations
        rsa_config = RSAConfig(bit_length=args.bits, r=args.r, s=args.s)
        
        # Auto-select m, t if not specified
        if args.m is None or args.t is None:
            from config import get_attack_params_for_bit_length
            m, t = get_attack_params_for_bit_length(args.bits)
        else:
            m, t = args.m, args.t
        
        exp_config = ExperimentConfig(
            delta=args.delta,
            exposure_type=args.type,
            m=m,
            t=t,
            description=f"{args.bits}-bit, {args.delta*100:.0f}% {args.type}"
        )
        
        success = run_single_attack(rsa_config, exp_config, verbose=True)
        sys.exit(0 if success else 1)
    
    elif args.command == 'benchmark':
        config = BenchmarkConfig(
            num_trials=args.trials,
            bit_lengths=args.bits,
            deltas=args.deltas
        )
        run_benchmark(config)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

