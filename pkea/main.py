from rsa_generator import RSAGenerator
from key_exposure import KeyExposure
from attack_worker import AttackWorker
from result_verifier import ResultVerifier
from config import CONFIG, BENCHMARK_CONFIGS


class PartialKeyAttackDemo:
    """Main demonstration class"""

    def __init__(self):
        self.rsa_gen = RSAGenerator()
        self.key_exposure = KeyExposure()
        self.attack_worker = AttackWorker()
        self.verifier = ResultVerifier()

    def run_demo(self):
        """Run main demonstration"""
        print("PP-RSA Partial Key Exposure Attack Demonstration")
        print("Targeting 128-bit N = p^r * q^s")
        print("=" * 60)

        print("Configuration parameters:")
        for key, value in CONFIG.items():
            print(f"  {key}: {value}")

        try:
            # 1. Generate PP-RSA parameters
            N, e, d, p, q, phi = self.rsa_gen.generate_pp_rsa(
                CONFIG['n_bits'], CONFIG['r'], CONFIG['s']
            )

            # 2. Create partial key exposure
            d0, x_true, X = self.key_exposure.create_partial_exposure(
                d, CONFIG['exposure_ratio'], CONFIG['exposure_type']
            )

            # 3. Execute attack
            x_recovered = self.attack_worker.multi_thread_attack(
                N, e, d0, X, phi,
                CONFIG['exposure_type'],
                CONFIG['num_threads'],
                CONFIG['timeout']
            )

            # 4. Verify results
            if x_recovered is not None:
                success = self.verifier.verify_attack(
                    N, e, d, d0, x_recovered, CONFIG['exposure_type']
                )
                print(f"\nFinal result: {'✓ Attack successful' if success else '✗ Attack failed'}")
            else:
                print(f"\nFinal result: ✗ Could not find solution within specified time")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

    def run_benchmarks(self):
        """Run benchmark tests"""
        print("\nPerformance test for different configurations")
        print("=" * 60)

        for config in BENCHMARK_CONFIGS:
            print(f"\n{config['desc']}:")
            print(f"  N bits: {config['n_bits']}, Exposure: {config['ratio'] * 100}%, Threads: {config['threads']}")

            try:
                N, e, d, p, q, phi = self.rsa_gen.generate_pp_rsa(config['n_bits'], 2, 1)
                d0, x_true, X = self.key_exposure.create_partial_exposure(d, config['ratio'], 'MSB')

                import time
                start_time = time.time()
                x_recovered = self.attack_worker.multi_thread_attack(
                    N, e, d0, X, phi, 'MSB', config['threads'], 30
                )
                elapsed = time.time() - start_time

                success = x_recovered == x_true if x_recovered is not None else False
                status = "✓ Success" if success else "✗ Failed"

                print(f"  Result: {status}, Time: {elapsed:.2f} seconds")

            except Exception as e:
                print(f"  Error: {e}")


if __name__ == "__main__":
    demo = PartialKeyAttackDemo()
    demo.run_demo()

    # Optional: run benchmark tests
    # demo.run_benchmarks()