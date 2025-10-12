from Crypto.Util.number import getPrime, inverse, GCD
from math_utils import MathUtils


class RSAGenerator:
    """PP-RSA parameter generator"""

    def __init__(self):
        pass

    def generate_pp_rsa(self, n_bits=128, r=2, s=1, e=65537):
        """Generate PP-RSA parameters N = p^r * q^s"""
        print(f"Generating {n_bits}-bit PP-RSA parameters: N = p^{r} * q^{s}")

        # Calculate bit lengths for p and q
        total_exp = r + s
        p_bits = n_bits * r // total_exp
        q_bits = n_bits * s // total_exp

        # Generate primes
        p = getPrime(p_bits)
        q = getPrime(q_bits)
        while p == q:
            q = getPrime(q_bits)

        # Calculate N and φ(N)
        N = (p ** r) * (q ** s)
        phi = MathUtils.calculate_phi(p, q, r, s)

        # Ensure e is coprime with φ(N)
        while GCD(e, phi) != 1:
            p = getPrime(p_bits)
            q = getPrime(q_bits)
            N = (p ** r) * (q ** s)
            phi = MathUtils.calculate_phi(p, q, r, s)

        d = inverse(e, phi)

        print(f"Generation completed:")
        print(f"  p = {p} ({p.bit_length()} bits)")
        print(f"  q = {q} ({q.bit_length()} bits)")
        print(f"  N = {N} ({N.bit_length()} bits)")
        print(f"  d = {d} ({d.bit_length()} bits)")

        return N, e, d, p, q, phi