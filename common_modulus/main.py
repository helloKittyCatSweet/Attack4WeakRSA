#!/usr/bin/env python3
"""
Common Modulus Attack - Main Entry Point

Supports multiple run modes:
1. paper   - Reproduce the paper example
2. demo    - Demonstrate the attack process
3. test    - Run demo test suite
4. unittest - Run unit tests
"""

import argparse
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from examples import run_paper_example, run_demo
from examples.demo_example import run_test_suite


def mode_paper():
    """Mode 1: Reproduce the paper example"""
    run_paper_example()


def mode_demo(args):
    """Mode 2: Demonstrate the attack process"""
    run_demo(bits=args.bits, e1=args.e1, e2=args.e2, message=args.message)


def mode_test():
    """Mode 3: Run the demo test suite"""
    run_test_suite()


def mode_unittest():
    """Mode 4: Run unit tests"""
    import unittest

    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Common Modulus Attack on RSA and ECC-RSA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  # Reproduce paper example
  python main.py --mode paper

  # Demo attack (512-bit RSA)
  python main.py --mode demo

  # Custom parameters for demo
  python main.py --mode demo --bits 1024 --e1 7 --e2 11 --message 987654321

  # Run demo test suite
  python main.py --mode test

  # Run unit tests
  python main.py --mode unittest
        """
    )

    parser.add_argument('--mode',
                        choices=['paper', 'demo', 'test', 'unittest'],
                        default='demo',
                        help='Run mode (Default: demo)')

    # Parameters for demo mode
    parser.add_argument('--bits', type=int, default=512,
                        help='RSA key bit length (Default: 512)')
    parser.add_argument('--e1', type=int, default=3,
                        help='First public exponent (Default: 3)')
    parser.add_argument('--e2', type=int, default=5,
                        help='Second public exponent (Default: 5)')
    parser.add_argument('--message', type=int, default=123456789,
                        help='Plaintext message (Default: 123456789)')

    args = parser.parse_args()

    # Execute according to mode
    try:
        if args.mode == 'paper':
            mode_paper()
        elif args.mode == 'demo':
            mode_demo(args)
        elif args.mode == 'test':
            mode_test()
        elif args.mode == 'unittest':
            sys.exit(mode_unittest())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
