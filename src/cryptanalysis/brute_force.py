
"""Brute-force attacks against classical ciphers."""

from src.classical.substitution import (
    shift_decrypt,
    affine_decrypt,
)
from src.mathematics.modular import gcd
from src.modern.des import (
    PC1_TABLE,
    encrypt_block_rounds,
)


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


def _effective_key_to_des_key(effective_key: int) -> int:
    """
    Convert a 56-bit effective DES key into a 64-bit DES key.

    The eight parity bits are set to zero.
    """
    if not isinstance(effective_key, int) or isinstance(effective_key, bool):
        raise TypeError("effective_key must be an integer")

    if not 0 <= effective_key < (1 << 56):
        raise ValueError("effective_key must fit in 56 bits")

    key = 0

    for index, position in enumerate(PC1_TABLE):
        bit = (effective_key >> (55 - index)) & 1
        key |= bit << (64 - position)

    return key


def brute_force_des_reduced(
    plaintext: int,
    ciphertext: int,
    rounds: int,
    key_bits: int,
) -> list[tuple[int, int]]:
    """
    Brute-force a reduced DES keyspace.

    The search enumerates key_bits leading bits of the
    56-bit effective DES key. Remaining bits are zero.

    Returns:
        A list of (effective_key, des_key) candidates
        that produce the given ciphertext.
    """
    if not isinstance(plaintext, int) or isinstance(plaintext, bool):
        raise TypeError("plaintext must be an integer")

    if not isinstance(ciphertext, int) or isinstance(ciphertext, bool):
        raise TypeError("ciphertext must be an integer")

    if not 0 <= plaintext < (1 << 64):
        raise ValueError("plaintext must fit in 64 bits")

    if not 0 <= ciphertext < (1 << 64):
        raise ValueError("ciphertext must fit in 64 bits")

    if not isinstance(rounds, int) or isinstance(rounds, bool):
        raise TypeError("rounds must be an integer")

    if not isinstance(key_bits, int) or isinstance(key_bits, bool):
        raise TypeError("key_bits must be an integer")

    if not 1 <= rounds <= 16:
        raise ValueError("rounds must be between 1 and 16")

    if not 1 <= key_bits <= 56:
        raise ValueError("key_bits must be between 1 and 56")

    candidates = []

    # Search all possible prefixes of the effective key.
    for candidate in range(1 << key_bits):
        effective_key = candidate << (56 - key_bits)

        # Convert the 56-bit effective key to a 64-bit DES key.
        des_key = _effective_key_to_des_key(effective_key)

        # Encrypt using reduced-round DES.
        result = encrypt_block_rounds(
            plaintext,
            des_key,
            rounds,
        )

        # Check whether the candidate key is correct.
        if result == ciphertext:
            candidates.append((effective_key, des_key))

    return candidates
