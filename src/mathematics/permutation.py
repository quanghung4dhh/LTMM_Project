
"""Permutation utilities for classical cryptography."""

from __future__ import annotations

from collections.abc import Sequence


def validate_permutation(permutation: Sequence[int]) -> int:
    """Validate a permutation of integers from 1 to n.

    A valid permutation must contain every integer from 1 to n
    exactly once, where n is the length of the sequence.

    Args:
        permutation: Sequence representing a permutation.

    Raises:
        TypeError: If the input is not a valid sequence of integers.
        ValueError: If the sequence is empty, contains duplicate
            values, or contains values outside the valid range.

    Examples:
        >>> validate_permutation([3, 1, 4, 2])
        >>> validate_permutation([1, 2, 3])
    """
    # Step 1: Validate the input container.
    if isinstance(permutation, (str, bytes)) or not isinstance(
        permutation, Sequence
    ):
        raise TypeError(
            "permutation must be a sequence of integers"
        )

    # Step 2: Reject an empty permutation.
    if len(permutation) == 0:
        raise ValueError("permutation must not be empty")

    n = len(permutation)

    # Step 3: Keep track of values that have already appeared.
    seen: set[int] = set()

    # Step 4: Validate each element.
    for index, value in enumerate(permutation):

        # Reject bool explicitly because bool is a subclass of int.
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(
                f"permutation[{index}] must be an integer, "
                f"got {type(value).__name__}"
            )

        # Every value must be between 1 and n.
        if not 1 <= value <= n:
            raise ValueError(
                f"permutation[{index}] must be between 1 and {n}, "
                f"got {value}"
            )

        # Duplicate values are not allowed.
        if value in seen:
            raise ValueError(
                f"duplicate value {value} in permutation"
            )

        seen.add(value)

    # Step 5: If valid, return the size of permutation
    return n


def inverse_permutation(permutation: Sequence[int]) -> list[int]:
    """Calculate the inverse of a valid permutation.

    The inverse permutation reverses the positional mapping of the
    original permutation.

    If the original permutation is P, the inverse Q satisfies:
        Q[P[i] - 1] = i + 1

    Args:
        permutation: Valid permutation of integers from 1 to n.

    Returns:
        A list representing the inverse permutation.

    Raises:
        TypeError: If the input or its elements have invalid types.
        ValueError: If the input is not a valid permutation.

    Examples:
        >>> inverse_permutation([3, 1, 4, 2])
        [2, 4, 1, 3]

        >>> inverse_permutation([1, 2, 3])
        [1, 2, 3]
    """
    # Step 1: Validate the input permutation.
    n = validate_permutation(permutation)

    # Step 2: Initialize the inverse permutation.
    inverse = [0] * n

    # Step 3: Reverse the positional mapping.
    for position, value in enumerate(permutation, start=1):
        inverse[value - 1] = position

    # Step 4: Return the inverse permutation.
    return inverse
