"""Hill cipher implementation for classical cryptography.

This module uses column vectors and matrix multiplication over Z_26.
Only ASCII letters A-Z/a-z are encrypted; all other characters are preserved
and do not participate in block formation.

Because X padding is ambiguous without metadata, ``hill_encrypt`` returns
both the ciphertext and the number of padding letters appended. Pass that
padding length to ``hill_decrypt`` to recover the exact original plaintext.
"""

from __future__ import annotations

from collections.abc import Sequence

from src.classical.common import (
    ALPHABET_SIZE,
    char_to_number,
    iter_alpha_positions,
    number_to_char,
)
from src.mathematics.matrix import (
    determinant,
    matrix_inverse_mod,
    matrix_multiply_mod,
    validate_matrix,
)
from src.mathematics.modular import gcd


MODULUS = ALPHABET_SIZE
PADDING_CHAR = "X"
PADDING_VALUE = char_to_number(PADDING_CHAR)
Matrix = Sequence[Sequence[int]]


def _prepare_key_matrix(
    key_matrix: Matrix, *, need_inverse: bool
) -> tuple[list[list[int]], list[list[int]] | None, int]:
    """Validate a Hill key and return (normalized key, optional inverse, size).

    Hill Cipher in this project requires a square matrix of size at least 2.
    A valid key must be invertible modulo 26. The inverse is calculated only
    during decryption, where it is actually needed.
    """
    rows, columns = validate_matrix(key_matrix, square=True)
    if rows < 2:
        raise ValueError("Hill key matrix must be at least 2x2")

    normalized_key = [
        [entry % MODULUS for entry in row]
        for row in key_matrix
    ]

    matrix_determinant = determinant(normalized_key)
    if gcd(matrix_determinant, MODULUS) != 1:
        raise ValueError(
            "Hill key matrix must be invertible modulo 26; "
            f"gcd(det(K), 26) = {gcd(matrix_determinant, MODULUS)}, not 1"
        )

    inverse_key = (
        matrix_inverse_mod(normalized_key, MODULUS) if need_inverse else None
    )
    return normalized_key, inverse_key, rows


def _validate_text(text: str, name: str) -> None:
    if not isinstance(text, str):
        raise TypeError(f"{name} must be a string, got {type(text).__name__}")


def hill_encrypt(plaintext: str, key_matrix: Matrix) -> tuple[str, int]:
    """Encrypt text using the Hill cipher.

    The encryption rule is ``C = K * P (mod 26)`` where each plaintext block
    is a column vector. The key must be a square, invertible matrix of size
    at least 2. If the number of ASCII letters is not divisible by the block
    size, uppercase X characters are appended as padding.

    Returns:
        A pair ``(ciphertext, padding_length)``. The padding length is needed
        for unambiguous decryption because the original plaintext may itself
        end in X.

    Only ASCII letters are transformed. Whitespace, punctuation, digits and
    non-ASCII characters are preserved and do not consume block positions.
    Ciphertext padding is appended after the original text.

    Raises:
        TypeError: If plaintext or a matrix element has an invalid type.
        ValueError: If the key matrix is invalid or not invertible modulo 26.

    Example:
        >>> hill_encrypt("HELP", [[3, 3], [2, 5]])
        ('HIAT', 0)
    """
    _validate_text(plaintext, "plaintext")
    normalized_key, _, block_size = _prepare_key_matrix(
        key_matrix, need_inverse=False
    )

    positions = list(iter_alpha_positions(plaintext))
    plaintext_values = [char_to_number(char) for _, char in positions]
    padding_length = (-len(plaintext_values)) % block_size
    plaintext_values.extend([PADDING_VALUE] * padding_length)

    ciphertext_values: list[int] = []
    for start in range(0, len(plaintext_values), block_size):
        block = plaintext_values[start: start + block_size]
        # Hill convention used here: each block is a column vector (n x 1).
        plaintext_vector = [[value] for value in block]
        encrypted_vector = matrix_multiply_mod(
            normalized_key, plaintext_vector, MODULUS
        )
        ciphertext_values.extend(row[0] for row in encrypted_vector)

    result = list(plaintext)
    original_letter_count = len(positions)

    for alpha_index, (text_index, char) in enumerate(positions):
        result[text_index] = number_to_char(
            ciphertext_values[alpha_index],
            uppercase=("A" <= char <= "Z"),
        )

    # Padding letters are appended after the original text so that a caller
    # can remove exactly these final letters using the returned metadata.
    padding_text = "".join(
        number_to_char(value)
        for value in ciphertext_values[original_letter_count:]
    )
    return "".join(result) + padding_text, padding_length


def hill_decrypt(
    ciphertext: str,
    key_matrix: Matrix,
    *,
    padding_length: int = 0,
) -> str:
    """Decrypt Hill ciphertext using the modular inverse of the key matrix.

    The decryption rule is ``P = K^(-1) * C (mod 26)``. Supply the exact
    ``padding_length`` returned by ``hill_encrypt`` to remove only the X
    characters added during encryption. If omitted, no padding is removed.

    The number of ASCII letters in ciphertext must be divisible by the key
    matrix dimension. Punctuation and other non-ASCII characters are kept in
    their original positions and do not participate in the blocks.

    Raises:
        TypeError: If ciphertext, padding_length, or matrix entries have
            invalid types.
        ValueError: If the key is invalid, ciphertext length is incompatible,
            padding_length is out of range, or the decrypted padding does not
            match the expected X suffix.

    Example:
        >>> hill_decrypt("HIAT", [[3, 3], [2, 5]])
        'HELP'
    """
    _validate_text(ciphertext, "ciphertext")
    if isinstance(padding_length, bool) or not isinstance(padding_length, int):
        raise TypeError(
            "padding_length must be an integer, "
            f"got {type(padding_length).__name__}"
        )

    _, inverse_key, block_size = _prepare_key_matrix(
        key_matrix, need_inverse=True
    )
    assert inverse_key is not None
    if not 0 <= padding_length < block_size:
        raise ValueError(
            f"padding_length must be between 0 and {block_size - 1}"
        )

    positions = list(iter_alpha_positions(ciphertext))
    ciphertext_values = [char_to_number(char) for _, char in positions]

    if len(ciphertext_values) % block_size != 0:
        raise ValueError(
            "ciphertext letter count must be divisible by the key matrix size "
            f"({block_size})"
        )
    if padding_length > len(ciphertext_values):
        raise ValueError(
            "padding_length cannot exceed the ciphertext letter count")

    plaintext_values: list[int] = []
    for start in range(0, len(ciphertext_values), block_size):
        block = ciphertext_values[start: start + block_size]
        ciphertext_vector = [[value] for value in block]
        decrypted_vector = matrix_multiply_mod(
            inverse_key, ciphertext_vector, MODULUS
        )
        plaintext_values.extend(row[0] for row in decrypted_vector)

    result = list(ciphertext)
    for alpha_index, (text_index, char) in enumerate(positions):
        result[text_index] = number_to_char(
            plaintext_values[alpha_index],
            uppercase=("A" <= char <= "Z"),
        )

    plaintext = "".join(result)
    if padding_length:
        expected_padding = PADDING_CHAR * padding_length
        if not plaintext.endswith(expected_padding):
            raise ValueError(
                "decrypted text does not end with the expected X padding; "
                "check padding_length or ciphertext integrity"
            )
        plaintext = plaintext[:-padding_length]

    return plaintext
