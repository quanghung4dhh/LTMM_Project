"""Plaintext Autokey cipher implementation.

This module implements the plaintext-autokey variant: the initial seed key
is followed by plaintext characters to form the keystream. The seed key is
not repeated. Only ASCII letters A-Z/a-z consume keystream positions.
"""

from __future__ import annotations

from src.classical.common import (
    ALPHABET_SIZE,
    char_to_number,
    iter_alpha_positions,
    normalize_alpha_key,
    number_to_char,
)
from src.mathematics.modular import add_mod, subtract_mod


MODULUS = ALPHABET_SIZE


def _autokey_text(text: str, seed_key: str, *, decrypt: bool) -> str:
    """Apply plaintext Autokey to ASCII letters in *text*.

    For letter index i and seed length r, the keystream value is:
      - seed_key[i], when i < r;
      - plaintext[i-r], when i >= r.

    During decryption, plaintext[i-r] is taken from the characters already
    recovered earlier in the same pass. Formatting and letter case are kept.

    Args:
        text: Plaintext for encryption or ciphertext for decryption.
        seed_key: Non-empty ASCII-letter seed key, normalized to uppercase.
        decrypt: Subtract the keystream when True; otherwise add it.

    Returns:
        Transformed text, preserving non-ASCII letters, digits, whitespace,
        punctuation, and the case of each ASCII letter.

    Raises:
        TypeError: If text or seed_key is not a string.
        ValueError: If seed_key is empty or contains non-ASCII letters.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    normalized_seed = normalize_alpha_key(seed_key)
    seed_values = tuple(char_to_number(char) for char in normalized_seed)

    # This list contains only cipher letters, not punctuation or whitespace.
    # Thus all key positions are indexed consistently with the Autokey rule.
    alpha_positions = list(iter_alpha_positions(text))
    plaintext_values = (
        [char_to_number(char) for _, char in alpha_positions]
        if not decrypt
        else []
    )
    recovered_plaintext_values: list[int] = []

    result = list(text)
    seed_length = len(seed_values)

    for alpha_index, (text_index, char) in enumerate(alpha_positions):
        # The seed is used only once. After that, append plaintext values.
        if alpha_index < seed_length:
            key_value = seed_values[alpha_index]
        elif decrypt:
            # The needed plaintext character was recovered seed_length
            # positions earlier, so it is already available.
            key_value = recovered_plaintext_values[alpha_index - seed_length]
        else:
            key_value = plaintext_values[alpha_index - seed_length]

        text_value = char_to_number(char)

        if decrypt:
            transformed_value = subtract_mod(
                text_value, key_value, MODULUS
            )
            recovered_plaintext_values.append(transformed_value)
        else:
            transformed_value = add_mod(
                text_value, key_value, MODULUS
            )

        result[text_index] = number_to_char(
            transformed_value,
            uppercase=("A" <= char <= "Z"),
        )

    return "".join(result)


def autokey_encrypt(plaintext: str, seed_key: str) -> str:
    """Encrypt using the plaintext-autokey variant of Autokey Cipher.

    The keystream is the seed key followed by the plaintext. The seed is not
    repeated. For each alphabetic character, ``C_i = (P_i + K_i) mod 26``.
    Only ASCII letters are transformed; all other characters are preserved
    and do not consume keystream positions.

    Example:
        >>> autokey_encrypt("ATTACKATDAWN", "QUEEN")
        'QNXEPKTMDCGN'

    Raises:
        TypeError: If plaintext or seed_key is not a string.
        ValueError: If seed_key is empty or contains non-ASCII letters.
    """
    return _autokey_text(plaintext, seed_key, decrypt=False)


def autokey_decrypt(ciphertext: str, seed_key: str) -> str:
    """Decrypt using the plaintext-autokey variant of Autokey Cipher.

    The seed is used for the first ``len(seed_key)`` alphabetic characters.
    Later keystream values come from plaintext characters already recovered.
    For each alphabetic character, ``P_i = (C_i - K_i) mod 26``.

    Example:
        >>> autokey_decrypt("QNXEPKTMDCGN", "QUEEN")
        'ATTACKATDAWN'

    Raises:
        TypeError: If ciphertext or seed_key is not a string.
        ValueError: If seed_key is empty or contains non-ASCII letters.
    """
    return _autokey_text(ciphertext, seed_key, decrypt=True)
