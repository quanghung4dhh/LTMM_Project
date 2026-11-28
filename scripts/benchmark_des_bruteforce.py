
import time
from statistics import median

from src.modern.des import encrypt_block_rounds
from src.cryptanalysis.brute_force import (
    brute_force_des_reduced,
    _effective_key_to_des_key,
)


def benchmark_des_brute_force():
    plaintext = 0x0123456789ABCDEF

    # The target key is inside every tested keyspace.
    effective_key = 0xA5000000000000
    des_key = _effective_key_to_des_key(effective_key)

    rounds = 4
    key_sizes = [8, 10, 12, 14]
    repetitions = 3

    print("=" * 72)
    print("REDUCED-ROUND DES BRUTE FORCE BENCHMARK")
    print("=" * 72)

    print(f"Rounds: {rounds}")
    print(f"Plaintext: 0x{plaintext:016X}")
    print(f"Effective key: 0x{effective_key:014X}")
    print(f"DES key: 0x{des_key:016X}")
    print()

    # Generate ciphertext before measuring attack time.
    ciphertext = encrypt_block_rounds(
        plaintext,
        des_key,
        rounds,
    )

    print(f"Ciphertext: 0x{ciphertext:016X}")
    print()

    print(
        f"{'Key bits':<12}"
        f"{'Candidates':<18}"
        f"{'Median time (s)':<20}"
        f"{'Found':<10}"
    )
    print("-" * 60)

    for key_bits in key_sizes:
        elapsed_times = []
        results = []

        for _ in range(repetitions):
            start = time.perf_counter()

            results = brute_force_des_reduced(
                plaintext,
                ciphertext,
                rounds,
                key_bits,
            )

            elapsed = time.perf_counter() - start
            elapsed_times.append(elapsed)

        elapsed_median = median(elapsed_times)
        candidate_count = 1 << key_bits

        found = any(
            candidate_key == effective_key
            for candidate_key, _ in results
        )

        print(
            f"{key_bits:<12}"
            f"{candidate_count:<18,}"
            f"{elapsed_median:<20.6f}"
            f"{str(found):<10}"
        )

    print("=" * 72)


if __name__ == "__main__":
    benchmark_des_brute_force()
