
"""Brute-force attacks against classical ciphers."""

from src.classical.substitution import (
    shift_decrypt,
    affine_decrypt,
)
from src.mathematics.modular import gcd
from src.classical.substitution import shift_decrypt


def brute_force_caesar(ciphertext: str) -> list[tuple[int, str]]:
    """
    Try every possible key to decrypt a Caesar cipher.

    Args:
        ciphertext: The ciphertext to decrypt.

    Returns:
        A list of (key, plaintext) tuples for keys from 0 to 25.

    Raises:
        TypeError: If ciphertext is not a string.
    """
    if not isinstance(ciphertext, str):
        raise TypeError(
            f"ciphertext must be a string, got {type(ciphertext).__name__}"
        )

    candidates = []

    # Caesar cipher has exactly 26 possible keys.
    for key in range(26):
        # Reuse the existing Caesar decryption implementation.
        plaintext = shift_decrypt(ciphertext, key)

        # Store the key and its corresponding plaintext.
        candidates.append((key, plaintext))

    return candidates


def brute_force_affine(
    ciphertext: str
) -> list[tuple[int, int, str]]:
    """
    Try every valid key pair to decrypt an Affine cipher.

    Args:
        ciphertext: The ciphertext to decrypt.

    Returns:
        A list of (a, b, plaintext) tuples for all valid
        Affine key pairs.

    Raises:
        TypeError: If ciphertext is not a string.
    """
    if not isinstance(ciphertext, str):
        raise TypeError(
            f"ciphertext must be a string, got {type(ciphertext).__name__}"
        )

    candidates = []

    # Iterate through all possible multiplicative keys.
    # A valid 'a' must be relatively prime to 26.
    for a in range(26):
        if gcd(a, 26) != 1:
            continue

        # Try all 26 possible additive keys.
        for b in range(26):
            # Decrypt using the current key pair.
            plaintext = affine_decrypt(ciphertext, a, b)

            # Store the key pair and corresponding plaintext.
            candidates.append((a, b, plaintext))

    return candidates
