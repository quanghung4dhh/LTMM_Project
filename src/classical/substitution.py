"""Monoalphabetic substitution ciphers.

This module currently implements the Shift (Caesar) cipher. Multiplicative
and Affine ciphers will be added here in later steps.
"""

from __future__ import annotations

from src.classical.common import (
    ALPHABET_SIZE,
    char_to_number,
    iter_alpha_positions,
    number_to_char,
)
from src.mathematics.modular import add_mod, normalize_mod, subtract_mod


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
        plain_or_cipher_value = char_to_number(char)

        if decrypt:
            transformed_value = subtract_mod(
                plain_or_cipher_value, normalized_key, MODULUS
            )
        else:
            transformed_value = add_mod(
                plain_or_cipher_value, normalized_key, MODULUS
            )

        # Keep the original letter's case in the transformed output.
        result[index] = number_to_char(
            transformed_value,
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

    Examples:
        >>> shift_decrypt("DWWDFN", 3)
        'ATTACK'
        >>> shift_decrypt("Khoor, Zruog!", 3)
        'Hello, World!'

    Raises:
        TypeError: If ciphertext is not a string or key is not an integer.
    """
    return _shift_text(ciphertext, key, decrypt=True)
