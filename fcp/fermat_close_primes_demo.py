import argparse
import math
import os
import random
import sys
import time


def miller_rabin(n: int, rounds: int = 16) -> bool:
    """Probabilistic primality test. True means 'probably prime'.

    For the purposes of this assignment/demo, 16 rounds is ample.
    """
    if n < 2:
        return False
    # Small primes shortcut
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    # write n-1 = d * 2^s with d odd
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # random bases in [2, n-2]
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def next_prime(start: int) -> int:
    """Return the smallest prime >= start (adjusting to odd)."""
    n = start
    if n <= 2:
        return 2
    if n % 2 == 0:
        n += 1
    while not miller_rabin(n):
        n += 2
    return n


def gen_close_primes(bits: int = 60, max_gap: int = 1 << 14) -> tuple[int, int]:
    """Generate two primes of ~`bits` bits where |p-q| <= max_gap.

    Strategy: pick a random prime p in [2^(bits-1), 2^bits), then move forward by
    a random even delta in [2, max_gap] and take the next prime as q.
    This typically produces q very close to p.
    """
    if bits < 8:
        raise ValueError("Use at least 8 bits for a meaningful demo")
    lo = 1 << (bits - 1)
    hi = (1 << bits) - 1
    while True:
        p_candidate = random.randrange(lo, hi)
        p = next_prime(p_candidate)
        # Make sure we didn't overshoot bit length too much
        if p.bit_length() != bits:
            continue
        # delta must be even to stay on odd numbers for step-by-2 scanning
        delta = random.randrange(2, max(4, max_gap + 1))
        if delta % 2 == 1:
            delta += 1
        q = next_prime(p + delta)
        if q.bit_length() == bits and q != p:
            return (p, q) if p < q else (q, p)


def fermat_factor(n: int, max_steps: int | None = None) -> tuple[int, int] | None:
    """Fermat factorization for odd n.

    Returns (p, q) if a factorization is found where n = p*q and p<=q.
    If max_steps is given and exceeded, returns None.
    """
    if n % 2 == 0:
        return (2, n // 2)
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    steps = 0
    while True:
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            p = a - b
            q = a + b
            if p * q == n:
                return (p, q) if p <= q else (q, p)
        a += 1
        steps += 1
        if max_steps is not None and steps > max_steps:
            return None


def human_readable_int(n: int) -> str:
    return f"{n:,}".replace(",", "_")


def run_demo(bits: int, max_gap: int, rounds: int) -> None:
    print(f"Generating ~{bits}-bit close primes with max_gap={max_gap}...")
    p, q = gen_close_primes(bits=bits, max_gap=max_gap)
    gap = abs(p - q)
    n = p * q
    print(f"p bit_length={p.bit_length()}  q bit_length={q.bit_length()}")
    print(f"p = {human_readable_int(p)}")
    print(f"q = {human_readable_int(q)}")
    print(f"|q-p| = {gap}  (steps ≈ {gap // 2} in Fermat)")
    print(f"n = p*q has {n.bit_length()} bits")

    # Factor via Fermat
    print("\nFactoring n with Fermat...")
    t0 = time.perf_counter()
    recovered = fermat_factor(n)
    t1 = time.perf_counter()
    if recovered is None:
        print("Fermat failed (unexpected in this demo)")
        return
    rp, rq = recovered
    ok = (rp == p and rq == q) or (rp == q and rq == p)
    print(f"Recovered p, q correctly: {ok}")
    print(f"Time: {(t1 - t0)*1000:.3f} ms")

    # Optionally run multiple trials to see typical timing
    if rounds > 1:
        print(f"\nRunning {rounds} trials for timing (new primes each time)...")
        times = []
        for _ in range(rounds):
            p, q = gen_close_primes(bits=bits, max_gap=max_gap)
            n = p * q
            t0 = time.perf_counter()
            fermat_factor(n)
            t1 = time.perf_counter()
            times.append(t1 - t0)
        avg_ms = sum(times) / len(times) * 1000
        best_ms = min(times) * 1000
        worst_ms = max(times) * 1000
        print(f"Fermat timing over {rounds} runs: avg={avg_ms:.2f} ms, best={best_ms:.2f} ms, worst={worst_ms:.2f} ms")


# ===== RSA end-to-end demo (encrypt -> factor -> decrypt) =====

def _egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = _egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def _inv_mod(a: int, m: int) -> int:
    a %= m
    g, x, _ = _egcd(a, m)
    if g != 1:
        raise ValueError("No modular inverse for given inputs")
    return x % m


def rsa_keygen_close(bits: int, max_gap: int, e: int = 65537) -> tuple[int, int, int, int, int]:
    """Return (n, e, d, p, q) using very-close primes for demo."""
    while True:
        p, q = gen_close_primes(bits=bits, max_gap=max_gap)
        phi = (p - 1) * (q - 1)
        if math.gcd(e, phi) == 1:
            d = _inv_mod(e, phi)
            return (p * q, e, d, p, q)


def _bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, "big")


def _int_to_bytes(x: int) -> bytes:
    if x == 0:
        return b"\x00"
    l = (x.bit_length() + 7) // 8
    return x.to_bytes(l, "big")


def run_rsa_demo(bits: int, max_gap: int, message: str) -> None:
    print(f"Generating RSA key with close primes (~{bits} bits each)...")
    n, e, d, p, q = rsa_keygen_close(bits=bits, max_gap=max_gap, e=65537)
    print(f"n bits = {n.bit_length()}  e = {e}")

    m = _bytes_to_int(message.encode("utf-8"))
    if m >= n:
        raise ValueError("Message too large for modulus. Use more bits or shorter message.")

    c = pow(m, e, n)
    print(f"Plaintext int m = {m}")
    print(f"Ciphertext int c = {c}")

    print("\nAttacker factors n with Fermat...")
    t0 = time.perf_counter()
    fp, fq = fermat_factor(n)
    t1 = time.perf_counter()
    assert fp * fq == n
    print(f"Recovered p and q in {(t1 - t0)*1000:.3f} ms; |q-p| = {abs(fp-fq)}")

    phi_rec = (fp - 1) * (fq - 1)
    d_rec = _inv_mod(e, phi_rec)
    m_dec = pow(c, d_rec, n)
    text = _int_to_bytes(m_dec).decode("utf-8", errors="replace")
    print(f"Decrypted m' = {m_dec}")
    print(f"Decrypted text: {text}")
    print(f"Match: {m_dec == m}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Demonstrate Fermat factorization on an RSA modulus with artificially close primes."
        )
    )
    parser.add_argument("--bits", type=int, default=60, help="Bit-length of primes to generate (default: 60)")
    parser.add_argument(
        "--max-gap",
        type=int,
        default=1 << 14,
        help="Maximum distance between p and q (default: 16384)",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=1,
        help="Number of independent trials for timing (default: 1)",
    )
    parser.add_argument(
        "--mode",
        choices=["fermat", "rsa"],
        default="fermat",
        help="Demo mode: 'fermat' (factor timing) or 'rsa' (encrypt->factor->decrypt)",
    )
    parser.add_argument(
        "--message",
        type=str,
        default="NTU close-primes RSA demo",
        help="Plaintext for RSA demo (utf-8)",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.bits >= 512 and args.max_gap > (1 << 20):
        print(
            "Warning: Extremely large parameters may take a long time. Consider smaller bits or gap.",
            file=sys.stderr,
        )
    if args.mode == "fermat":
        run_demo(bits=args.bits, max_gap=args.max_gap, rounds=args.rounds)
    else:
        run_rsa_demo(bits=args.bits, max_gap=args.max_gap, message=args.message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
