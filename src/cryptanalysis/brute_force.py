
"""Brute-force attacks against classical ciphers."""

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
