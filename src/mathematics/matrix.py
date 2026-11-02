"""Matrix operations for classical cryptography.

The functions in this module operate on matrices represented as lists of lists
(or other sequence-of-sequences objects) containing integers.  Modular
operations accept any modulus >= 2; they are not limited to modulo 26.

The module is intended to support Hill Cipher and other algorithms that need
matrix arithmetic over the residue ring Z_n.
"""

from __future__ import annotations

from collections.abc import Sequence

from src.mathematics.modular import mod_inverse


Matrix = Sequence[Sequence[int]]


def _require_integer(name: str, value: int) -> None:
    """Raise TypeError unless value is an integer (but not a bool)."""
    # bool is a subclass of int in Python.  Reject it to avoid silently
    # accepting True/False as matrix entries or moduli.
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(
            f"{name} must be an integer, got {type(value).__name__}")


def _require_modulus(modulus: int) -> None:
    """Validate the modulus used by cryptographic matrix operations."""
    _require_integer("modulus", modulus)
    if modulus < 2:
        raise ValueError(f"modulus must be >= 2, got {modulus}")


def validate_matrix(matrix: Matrix, *, square: bool = False) -> tuple[int, int]:
    """Validate a non-empty rectangular integer matrix and return its shape.

    Args:
        matrix: Matrix represented by rows of integer values.
        square: When True, require the number of rows to equal the number of
            columns.

    Returns:
        A ``(row_count, column_count)`` tuple.

    Raises:
        TypeError: If the matrix, a row, or an element has an invalid type.
        ValueError: If the matrix is empty, ragged, or non-square when
            ``square=True``.

    This function validates without changing or copying the input matrix.
    """
    # Strings technically behave like sequences, but they are not useful
    # matrix containers for this API.
    if isinstance(matrix, (str, bytes)) or not isinstance(matrix, Sequence):
        raise TypeError("matrix must be a sequence of rows")

    if len(matrix) == 0:
        raise ValueError("matrix must contain at least one row")

    column_count: int | None = None

    for row_index, row in enumerate(matrix):
        if isinstance(row, (str, bytes)) or not isinstance(row, Sequence):
            raise TypeError(f"row {row_index} must be a sequence of integers")

        if len(row) == 0:
            raise ValueError(
                f"row {row_index} must contain at least one element")

        if column_count is None:
            column_count = len(row)
        elif len(row) != column_count:
            raise ValueError(
                "matrix must be rectangular; all rows must have equal length")

        for column_index, value in enumerate(row):
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(
                    f"matrix[{row_index}][{column_index}] must be an integer, "
                    f"got {type(value).__name__}"
                )

    # At this point the matrix has at least one non-empty row.
    assert column_count is not None
    row_count = len(matrix)

    if square and row_count != column_count:
        raise ValueError(
            f"matrix must be square, got {row_count} rows and {column_count} columns"
        )

    return row_count, column_count


def matrix_add_mod(left: Matrix, right: Matrix, modulus: int) -> list[list[int]]:
    """Add two same-shaped matrices element by element modulo ``modulus``.

    Negative entries are allowed.  Each result entry is normalized into the
    range ``0 .. modulus - 1``.
    """
    _require_modulus(modulus)
    left_rows, left_columns = validate_matrix(left)
    right_rows, right_columns = validate_matrix(right)

    if (left_rows, left_columns) != (right_rows, right_columns):
        raise ValueError(
            "matrices must have the same dimensions for addition; "
            f"got {left_rows}x{left_columns} and {right_rows}x{right_columns}"
        )

    return [
        [(left[i][j] + right[i][j]) % modulus for j in range(left_columns)]
        for i in range(left_rows)
    ]


def matrix_multiply_mod(
    left: Matrix, right: Matrix, modulus: int
) -> list[list[int]]:
    """Multiply two compatible matrices modulo ``modulus``.

    If ``left`` has shape ``r x k`` and ``right`` has shape ``k x c``, the
    returned matrix has shape ``r x c``.  The dot product is calculated using
    ordinary integer arithmetic and then reduced modulo ``modulus``.
    """
    _require_modulus(modulus)
    left_rows, left_columns = validate_matrix(left)
    right_rows, right_columns = validate_matrix(right)

    if left_columns != right_rows:
        raise ValueError(
            "incompatible matrix dimensions for multiplication; "
            f"left has {left_rows}x{left_columns}, "
            f"right has {right_rows}x{right_columns}"
        )

    result: list[list[int]] = []
    for i in range(left_rows):
        result_row: list[int] = []
        for j in range(right_columns):
            # Matrix multiplication: row i of the left matrix dotted with
            # column j of the right matrix.
            dot_product = sum(
                left[i][k] * right[k][j] for k in range(left_columns)
            )
            result_row.append(dot_product % modulus)
        result.append(result_row)

    return result


def _determinant_unchecked(square_matrix: Sequence[Sequence[int]]) -> int:
    """Calculate a determinant with Bareiss' fraction-free elimination.

    The caller must provide a square matrix.  The empty 0x0 determinant is
    defined as 1 here because it occurs when calculating cofactors of a 1x1
    matrix.

    Bareiss elimination keeps intermediate values as integers and, unlike a
    floating-point method, avoids rounding errors.  Row swaps are used when a
    pivot is zero.
    """
    size = len(square_matrix)

    if size == 0:
        return 1
    if size == 1:
        return square_matrix[0][0]

    # Work on a copy: determinant calculation must not mutate caller data.
    values = [list(row) for row in square_matrix]
    sign = 1
    previous_pivot = 1

    for pivot_index in range(size - 1):
        # Find a non-zero pivot in the current column.  If none exists below
        # this point, the determinant is zero.
        pivot_row = next(
            (
                row_index
                for row_index in range(pivot_index, size)
                if values[row_index][pivot_index] != 0
            ),
            None,
        )
        if pivot_row is None:
            return 0

        # Swapping rows changes the sign of the determinant.
        if pivot_row != pivot_index:
            values[pivot_index], values[pivot_row] = (
                values[pivot_row],
                values[pivot_index],
            )
            sign *= -1

        pivot = values[pivot_index][pivot_index]

        # Update the lower-right submatrix using Bareiss' fraction-free step:
        # new[i][j] = (old[i][j] * pivot - old[i][k] * old[k][j]) / previous_pivot
        for row_index in range(pivot_index + 1, size):
            for column_index in range(pivot_index + 1, size):
                numerator = (
                    values[row_index][column_index] * pivot
                    - values[row_index][pivot_index]
                    * values[pivot_index][column_index]
                )

                # For exact integer input, Bareiss' algorithm guarantees that
                # this division has no remainder (including after row swaps).
                quotient, remainder = divmod(numerator, previous_pivot)
                if remainder != 0:  # Defensive guard against implementation errors.
                    raise ArithmeticError(
                        "Bareiss elimination lost exact divisibility")
                values[row_index][column_index] = quotient

            # Entries below the pivot are no longer needed.
            values[row_index][pivot_index] = 0

        previous_pivot = pivot

    return sign * values[size - 1][size - 1]


def determinant(matrix: Matrix) -> int:
    """Return the exact integer determinant of a non-empty square matrix.

    The determinant is returned as an ordinary integer, not reduced modulo
    ``modulus``.  This matters because invertibility modulo n is determined by
    checking ``gcd(determinant(matrix), n) == 1``.
    """
    validate_matrix(matrix, square=True)
    return _determinant_unchecked(matrix)


def matrix_inverse_mod(matrix: Matrix, modulus: int) -> list[list[int]]:
    """Return the inverse of a square matrix over ``Z_modulus``.

    A matrix is invertible modulo ``modulus`` exactly when its determinant is
    relatively prime to the modulus.  The implementation uses
    ``A^-1 = det(A)^-1 * adj(A)`` modulo the modulus, where ``adj(A)`` is the
    transpose of the cofactor matrix.

    Raises:
        TypeError: If the matrix or modulus contains non-integer values.
        ValueError: If the matrix is not square or has no inverse modulo the
            requested modulus.
    """
    _require_modulus(modulus)
    size, _ = validate_matrix(matrix, square=True)

    matrix_determinant = determinant(matrix)

    # Reuse the shared modular arithmetic implementation rather than
    # duplicating the Extended Euclidean Algorithm here.
    try:
        determinant_inverse = mod_inverse(matrix_determinant, modulus)
    except ValueError as error:
        raise ValueError(
            "matrix has no inverse modulo "
            f"{modulus}: gcd(det(matrix), {modulus}) is not 1 "
            f"(determinant = {matrix_determinant})"
        ) from error

    # First calculate every cofactor C[i][j].  The determinant of a 0x0 minor
    # is treated as 1 by _determinant_unchecked, which handles 1x1 matrices.
    cofactors = [[0] * size for _ in range(size)]
    for row_to_remove in range(size):
        for column_to_remove in range(size):
            minor = [
                [
                    matrix[row_index][column_index]
                    for column_index in range(size)
                    if column_index != column_to_remove
                ]
                for row_index in range(size)
                if row_index != row_to_remove
            ]

            cofactor = _determinant_unchecked(minor)
            if (row_to_remove + column_to_remove) % 2 == 1:
                cofactor = -cofactor
            cofactors[row_to_remove][column_to_remove] = cofactor

    # The adjugate is the transpose of the cofactor matrix.  Multiply each
    # entry by the modular inverse of the determinant and normalize it.
    inverse: list[list[int]] = []
    for row_index in range(size):
        inverse_row: list[int] = []
        for column_index in range(size):
            adjugate_entry = cofactors[column_index][row_index]
            inverse_row.append(
                (determinant_inverse * adjugate_entry) % modulus)
        inverse.append(inverse_row)

    return inverse
