class ResultVerifier:
    """Verify attack results"""

    def __init__(self):
        pass

    def verify_attack(self, N, e, d, d0, x_recovered, exposure_type):
        """Verify attack results"""
        print(f"\nVerifying attack results:")
        print("=" * 50)

        if x_recovered is None:
            print("Attack failed")
            return False

        # Reconstruct complete d
        d_recovered = self._reconstruct_d(d0, x_recovered, exposure_type)

        print(f"Original d: {d}")
        print(f"Recovered d: {d_recovered}")
        print(f"Match: {'✓' if d == d_recovered else '✗'}")

        # Run additional validations
        validations = self._run_validations(N, e, d, d_recovered)

        for test, result in validations.items():
            print(f"{test}: {'✓' if result else '✗'}")

        return d == d_recovered

    def _reconstruct_d(self, d0, x_recovered, exposure_type):
        """Reconstruct complete private key"""
        if exposure_type == "MSB":
            return d0 + x_recovered
        else:
            known_bits = d0.bit_length()
            return (x_recovered << known_bits) + d0

    def _run_validations(self, N, e, d, d_recovered):
        """Run various validations"""
        # Approximate φ(N)
        phi_approx = (e * d - 1) // ((e * d - 1) // N + 1)

        validations = {
            "Mathematical validation": (e * d_recovered - 1) % phi_approx == 0,
            "Encryption/decryption test": self._test_encryption(N, e, d_recovered)
        }

        return validations

    def _test_encryption(self, N, e, d_recovered):
        """Test encryption/decryption"""
        try:
            test_msg = 123456
            cipher = pow(test_msg, e, N)
            decrypted = pow(cipher, d_recovered, N)
            return test_msg == decrypted
        except:
            return False