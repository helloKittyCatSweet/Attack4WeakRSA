#!/usr/bin/env python3
"""
Main CLI entry point for Wiener Attack

Provides command-line interface with subcommands.
"""

import argparse
import sys

# Handle both direct and module execution
try:
    from runner import run_single_attack, run_comparison, run_demonstration
    from core import WeakRSAGenerator
except ImportError:
    from .runner import run_single_attack, run_comparison, run_demonstration
    from .core import WeakRSAGenerator


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Wiener Attack and Improvements",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run demonstration (shows both success and boundary cases)
  python main.py demo

  # Run single attack
  python main.py attack --bits 512 --type wiener

  # Compare all methods (all succeed)
  python main.py compare --bits 512 --d-ratio 0.24

  # Compare all methods (demonstrate boundaries)
  python main.py compare --bits 512 --d-ratio 0.25
        """
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration')
    
    # Attack command
    attack_parser = subparsers.add_parser('attack', help='Run single attack')
    attack_parser.add_argument('--bits', type=int, default=512,
                                help='Bit length of RSA modulus (default: 512)')
    attack_parser.add_argument('--type', type=str, default='wiener',
                                choices=['wiener', 'bunder_tonien', 'new_boundary'],
                                help='Attack type (default: wiener)')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare all attack methods')
    compare_parser.add_argument('--bits', type=int, default=512,
                                 help='Bit length of RSA modulus (default: 512)')
    compare_parser.add_argument('--d-ratio', type=float, default=0.24,
                                 help='d size ratio (0.24=all succeed, 0.25=show boundaries) (default: 0.24)')
    
    args = parser.parse_args()
    
    # Execute command
    if args.command == 'demo':
        run_demonstration()
    
    elif args.command == 'attack':
        # Generate weak RSA key
        print(f"Generating {args.bits}-bit RSA key vulnerable to {args.type} attack...")
        generator = WeakRSAGenerator()
        n, e, d, p, q, boundary = generator.generate_by_boundary(bits=args.bits, attack_type=args.type)
        
        print(f"\nGenerated RSA key:")
        print(f"  N: {n.bit_length()} bits")
        print(f"  d: {d.bit_length()} bits")
        print(f"  Boundary: {boundary}")
        print(f"  d < boundary: {'✓' if d < boundary else '✗'}")
        
        # Run attack
        print(f"\nRunning {args.type} attack...")
        success, time_ms = run_single_attack(n, e, d, args.type)
        
        sys.exit(0 if success else 1)
    
    elif args.command == 'compare':
        # Generate weak RSA key with configurable d size
        if args.d_ratio == 0.24:
            print(f"Generating {args.bits}-bit RSA key with very small d (all methods will succeed)...")
        elif args.d_ratio == 0.25:
            print(f"Generating {args.bits}-bit RSA key with medium d (demonstrating boundaries)...")
        else:
            print(f"Generating {args.bits}-bit RSA key with d_ratio={args.d_ratio}...")

        generator = WeakRSAGenerator()
        n, e, d, p, q = generator.generate_weak_rsa(bits=args.bits, d_ratio=args.d_ratio)

        # Run comparison
        results = run_comparison(n, e, d)

        # Check if all succeeded
        all_success = all(r['success'] for r in results.values())
        sys.exit(0 if all_success else 1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

