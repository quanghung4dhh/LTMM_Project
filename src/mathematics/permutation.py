
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
