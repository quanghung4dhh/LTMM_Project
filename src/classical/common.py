"""Shared helpers for classical substitution ciphers.

The project uses the 26-letter English alphabet and maps A..Z to 0..25.
Only ASCII English letters are treated as alphabetic cipher symbols.
All other characters (spaces, punctuation, digits, and non-ASCII letters)
are left untouched by text-processing algorithms that use this module.
"""

from __future__ import annotations

from collections.abc import Iterator


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_SIZE = len(ALPHABET)


def is_ascii_letter(char: str) -> bool:
    """Return whether *char* is exactly one ASCII English letter.

    A single character in ``A..Z`` or ``a..z`` returns True. An empty string,
    a multi-character string, punctuation, digits, and non-ASCII letters
    return False.

    Raises:
        TypeError: If *char* is not a string.
    """
    if not isinstance(char, str):
        raise TypeError(f"char must be a string, got {type(char).__name__}")

    return len(char) == 1 and (
        "A" <= char <= "Z" or "a" <= char <= "z"
    )


def char_to_number(char: str) -> int:
    """Convert one ASCII English letter to its value in ``Z_26``.

    The mapping is case-insensitive: A/a -> 0, B/b -> 1, ..., Z/z -> 25.

    Raises:
        TypeError: If *char* is not a string.
        ValueError: If *char* is not exactly one ASCII English letter.
    """
    if not isinstance(char, str):
        raise TypeError(f"char must be a string, got {type(char).__name__}")

    if not is_ascii_letter(char):
        raise ValueError(f"char must be one ASCII letter A-Z, got {char!r}")

    return ord(char.upper()) - ord("A")


def number_to_char(number: int, *, uppercase: bool = True) -> str:
    """Convert an integer in ``0..25`` to an English alphabet letter.

    Args:
        number: The canonical value of a letter in ``Z_26``.
        uppercase: Return an uppercase letter when True, otherwise lowercase.

    Raises:
        TypeError: If *number* is not an integer (or is a bool), or if
            *uppercase* is not a bool.
        ValueError: If *number* is outside the range ``0..25``.

    This function intentionally does not apply modulo 26. Callers should
    normalize arithmetic results with ``normalize_mod`` before conversion.
    """
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError(
            f"number must be an integer, got {type(number).__name__}"
        )

    if not isinstance(uppercase, bool):
        raise TypeError(
            f"uppercase must be a bool, got {type(uppercase).__name__}"
        )

    if not 0 <= number < ALPHABET_SIZE:
        raise ValueError(
            f"number must be between 0 and {ALPHABET_SIZE - 1}, got {number}"
        )

    letter = ALPHABET[number]
    return letter if uppercase else letter.lower()


def normalize_alpha_key(key: str) -> str:
    """Validate an ASCII-letter key and normalize it to uppercase.

    Keys must be non-empty and contain only ASCII letters A-Z/a-z.
    Whitespace, digits, punctuation, and non-ASCII letters are rejected
    rather than silently removed.

    Raises:
        TypeError: If *key* is not a string.
        ValueError: If *key* is empty or contains a non-ASCII-letter symbol.
    """
    if not isinstance(key, str):
        raise TypeError(f"key must be a string, got {type(key).__name__}")

    if key == "":
        raise ValueError("key must not be empty")

    for position, char in enumerate(key):
        if not is_ascii_letter(char):
            raise ValueError(
                "key must contain only ASCII letters A-Z; "
                f"invalid character {char!r} at position {position}"
            )

    return key.upper()


def iter_alpha_positions(text: str) -> Iterator[tuple[int, str]]:
    """Yield ``(index, character)`` for each ASCII letter in *text*.

    The original character and its case are preserved. Non-letter characters
    are skipped but their positions remain part of the original string.
    This lets Vigenere-like algorithms advance their key only on A-Z symbols
    while leaving spaces, punctuation, digits, and Unicode characters intact.

    Raises:
        TypeError: If *text* is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, got {type(text).__name__}")

    for index, char in enumerate(text):
        if is_ascii_letter(char):
            yield index, char
