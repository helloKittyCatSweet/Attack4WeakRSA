import math


class KeyExposure:
    """Handle partial key exposure scenarios"""

    def __init__(self):
        pass

    def create_partial_exposure(self, d, exposure_ratio=0.7, exposure_type="MSB"):
        """Create partial key exposure scenario"""
        d_bits = d.bit_length()
        unknown_bits = int(d_bits * (1 - exposure_ratio))

        print(f"\nCreating partial key exposure:")
        print(f"  Total bits: {d_bits}")
        print(f"  Exposure ratio: {exposure_ratio * 100}%")
        print(f"  Unknown bits: {unknown_bits}")

        if exposure_type == "MSB":
            d0, x, X = self._create_msb_exposure(d, unknown_bits)
        else:
            d0, x, X = self._create_lsb_exposure(d, d_bits, exposure_ratio, unknown_bits)

        print(f"  Known part d0 = {d0}")
        print(f"  Unknown part x = {x}")
        print(f"  Search bound X = {X} (2^{math.log2(X):.1f})")

        return d0, x, X

    def _create_msb_exposure(self, d, unknown_bits):
        """Create MSB exposure scenario"""
        shift = unknown_bits
        d0 = (d >> shift) << shift  # Known high bits
        x = d - d0  # Unknown low bits
        X = 2 ** shift  # Upper bound
        return d0, x, X

    def _create_lsb_exposure(self, d, d_bits, exposure_ratio, unknown_bits):
        """Create LSB exposure scenario"""
        known_bits = d_bits - unknown_bits
        mask = (1 << known_bits) - 1
        d0 = d & mask  # Known low bits
        x = d >> known_bits  # Unknown high bits
        X = 2 ** unknown_bits  # Upper bound
        return d0, x, X