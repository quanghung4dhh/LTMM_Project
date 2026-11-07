"""Vigenere cipher implementation for classical cryptography."""

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


def _vigenere_text(text: str, key: str, *, decrypt: bool) -> str:
    """Apply the repeating-key Vigenere transformation to *text*.

    Only ASCII letters A-Z/a-z are transformed. Whitespace, punctuation,
    digits, and non-ASCII letters are preserved and do not consume key
    characters. The original case of each transformed letter is preserved.

    Args:
        text: Plaintext to encrypt or ciphertext to decrypt.
        key: Non-empty ASCII-letter key. It is normalized to uppercase.
        decrypt: Subtract key values when True; add them otherwise.

    Returns:
        Transformed text with original formatting and letter case preserved.

    Raises:
        TypeError: If text or key is not a string.
        ValueError: If key is empty or contains non-ASCII-letter characters.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    normalized_key = normalize_alpha_key(key)
    key_values = tuple(char_to_number(char) for char in normalized_key)

    result = list(text)
    key_index = 0

    for text_index, char in iter_alpha_positions(text):
        text_value = char_to_number(char)
        key_value = key_values[key_index % len(key_values)]

        if decrypt:
            transformed_value = subtract_mod(
                text_value, key_value, MODULUS
            )
        else:
            transformed_value = add_mod(
                text_value, key_value, MODULUS
            )

        result[text_index] = number_to_char(
            transformed_value,
            uppercase=("A" <= char <= "Z"),
        )
        key_index += 1

    return "".join(result)


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt *plaintext* using the repeating-key Vigenere cipher.

    The encryption rule is ``C_i = (P_i + K_i) mod 26``. The key repeats
    over ASCII letters only; formatting characters are preserved and do
    not advance the key position.

    Examples:
        >>> vigenere_encrypt("ATTACKATDAWN", "LEMON")
        'LXFOPVEFRNHR'
        >>> vigenere_encrypt("Hello, World!", "KEY")
        'Rijvs, Uyvjn!'

    Raises:
        TypeError: If plaintext or key is not a string.
        ValueError: If key is empty or contains non-ASCII letters.
    """
    return _vigenere_text(plaintext, key, decrypt=False)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt *ciphertext* using the repeating-key Vigenere cipher.

    The decryption rule is ``P_i = (C_i - K_i) mod 26``. The same key
    progression and text-preservation rules as encryption are used.

    Examples:
        >>> vigenere_decrypt("LXFOPVEFRNHR", "LEMON")
        'ATTACKATDAWN'
        >>> vigenere_decrypt("Rijvs, Uyvjn!", "KEY")
        'Hello, World!'

    Raises:
        TypeError: If ciphertext or key is not a string.
        ValueError: If key is empty or contains non-ASCII letters.
    """
    return _vigenere_text(ciphertext, key, decrypt=True)
