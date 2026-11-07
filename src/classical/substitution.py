"""Monoalphabetic substitution ciphers.

This module implements the Shift (Caesar) and Multiplicative ciphers.
Affine Cipher can be added here in a later step.
"""

from __future__ import annotations

from src.classical.common import (
    ALPHABET_SIZE,
    char_to_number,
    iter_alpha_positions,
    number_to_char,
)
from src.mathematics.modular import (
    add_mod,
    gcd,
    mod_inverse,
    multiply_mod,
    normalize_mod,
    subtract_mod,
)


MODULUS = ALPHABET_SIZE


def _shift_text(text: str, key: int, *, decrypt: bool) -> str:
    """Apply a normalized Caesar shift to the ASCII letters in *text*.

    Non-ASCII letters, digits, whitespace, and punctuation are preserved.
    Letter case is preserved. The helper is shared by encryption and
    decryption so both operations follow exactly the same text-handling rules.

    Args:
        text: Text to transform.
        key: Any integer shift value; it is normalized modulo 26.
        decrypt: When True, subtract the key; otherwise, add it.

    Returns:
        Transformed text with the original formatting preserved.

    Raises:
        TypeError: If text is not a string or key is not an integer.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    # normalize_mod validates that key is an integer (and rejects bool) while
    # reducing negative or oversized keys to the canonical range 0..25.
    normalized_key = normalize_mod(key, MODULUS)

    # Work on a list so only alphabetic character positions need to change.
    # Spaces, punctuation, digits, and non-ASCII characters remain untouched.
    result = list(text)

    for index, char in iter_alpha_positions(text):
        value = char_to_number(char)
        if decrypt:
            transformed = subtract_mod(value, normalized_key, MODULUS)
        else:
            transformed = add_mod(value, normalized_key, MODULUS)

        # Keep the original letter's case in the transformed output.
        result[index] = number_to_char(
            transformed,
            uppercase=("A" <= char <= "Z"),
        )

    return "".join(result)


def shift_encrypt(plaintext: str, key: int) -> str:
    """Encrypt *plaintext* using the Shift (Caesar) cipher.

    The encryption rule is ``C = (P + key) mod 26``. Any integer key is
    accepted and normalized modulo 26. Only ASCII letters A-Z/a-z are
    transformed; all other characters and the original letter case are kept.

    Examples:
        >>> shift_encrypt("ATTACK", 3)
        'DWWDFN'
        >>> shift_encrypt("Hello, World!", 3)
        'Khoor, Zruog!'

    Raises:
        TypeError: If plaintext is not a string or key is not an integer.
    """
    return _shift_text(plaintext, key, decrypt=False)


def shift_decrypt(ciphertext: str, key: int) -> str:
    """Decrypt *ciphertext* using the Shift (Caesar) cipher.

    The decryption rule is ``P = (C - key) mod 26``. Any integer key is
    accepted and normalized modulo 26. Only ASCII letters A-Z/a-z are
    transformed; all other characters and the original letter case are kept.
    """
    return _shift_text(ciphertext, key, decrypt=True)


def _multiplicative_text(text: str, key: int, *, decrypt: bool) -> str:
    """Apply the Multiplicative cipher to the ASCII letters in *text*.

    The key is normalized modulo 26 and must be relatively prime to 26.
    During decryption, the normalized key is replaced by its modular inverse.
    Non-ASCII letters, digits, whitespace, and punctuation are preserved.

    Args:
        text: Text to transform.
        key: Integer multiplicative key.
        decrypt: When True, use the modular inverse of the key.

    Returns:
        Transformed text with its original formatting and letter case.

    Raises:
        TypeError: If text is not a string or key is not an integer.
        ValueError: If the key has no multiplicative inverse modulo 26.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    # Normalize first, so negative and oversized keys represent their
    # canonical residue in Z_26 (for example, 29 is equivalent to 3).
    normalized_key = normalize_mod(key, MODULUS)

    # Multiplication modulo 26 is reversible only for keys coprime to 26.
    common_divisor = gcd(normalized_key, MODULUS)
    if common_divisor != 1:
        raise ValueError(
            "key must be relatively prime to 26; "
            f"gcd({normalized_key}, 26) = {common_divisor}"
        )

    # Encryption multiplies by a. Decryption multiplies by a^(-1) instead.
    multiplier = (
        mod_inverse(normalized_key, MODULUS) if decrypt else normalized_key
    )

    result = list(text)
    for index, char in iter_alpha_positions(text):
        value = char_to_number(char)
        transformed = multiply_mod(value, multiplier, MODULUS)
        result[index] = number_to_char(
            transformed,
            uppercase=("A" <= char <= "Z"),
        )

    return "".join(result)


def multiplicative_encrypt(plaintext: str, key: int) -> str:
    """Encrypt *plaintext* using the Multiplicative cipher.

    The encryption rule is ``C = (key * P) mod 26``. The key may be any
    integer whose residue modulo 26 is coprime to 26. Only ASCII letters are
    transformed; all other characters and the original letter case remain.

    Examples:
        >>> multiplicative_encrypt("HELLO", 5)
        'JUDDS'
        >>> multiplicative_encrypt("Hello, World!", 5)
        'Judds, Gshdp!'

    Raises:
        TypeError: If plaintext is not a string or key is not an integer.
        ValueError: If the key is not invertible modulo 26.
    """
    return _multiplicative_text(plaintext, key, decrypt=False)


def multiplicative_decrypt(ciphertext: str, key: int) -> str:
    """Decrypt *ciphertext* using the Multiplicative cipher.

    The decryption rule is ``P = (key^(-1) * C) mod 26``. The key must be
    invertible modulo 26, meaning ``gcd(key, 26) == 1``.

    Examples:
        >>> multiplicative_decrypt("JUDDS", 5)
        'HELLO'

    Raises:
        TypeError: If ciphertext is not a string or key is not an integer.
        ValueError: If the key is not invertible modulo 26.
    """
    return _multiplicative_text(ciphertext, key, decrypt=True)
