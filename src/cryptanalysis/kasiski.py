
"""Kasiski examination utilities for classical cryptanalysis."""

from src.mathematics.modular import gcd
from collections import defaultdict


def find_repeated_ngrams(
    ciphertext: str,
    n: int = 3
) -> dict[str, list[int]]:
    """
    Find repeated n-grams and their starting positions in a ciphertext.

    Only ASCII English letters are considered. All valid letters are
    converted to uppercase before searching.

    Args:
        ciphertext: The ciphertext to analyze.
        n: The length of each n-gram. Defaults to 3.

    Returns:
        A dictionary mapping each repeated n-gram to its starting
        positions in the normalized ciphertext.

    Raises:
        TypeError: If ciphertext is not a string or n is not an integer.
        ValueError: If n is less than or equal to zero.
    """
    # 1. Validate ciphertext.
    if not isinstance(ciphertext, str):
        raise TypeError(
            f"ciphertext must be a string, got {type(ciphertext).__name__}"
        )

    # 2. Validate n.
    # bool is a subclass of int in Python, so it must be rejected explicitly.
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")

    if n <= 0:
        raise ValueError("n must be greater than zero")

    # 3. Normalize ciphertext:
    #    - Keep only ASCII English letters.
    #    - Convert lowercase letters to uppercase.
    normalized = "".join(
        char.upper()
        for char in ciphertext
        if ("A" <= char <= "Z") or ("a" <= char <= "z")
    )

    # 4. Store the positions of each n-gram.
    positions = defaultdict(list)

    # 5. Use a sliding window to extract n-grams.
    #    The step size is 1, so overlapping n-grams are allowed.
    for i in range(len(normalized) - n + 1):
        ngram = normalized[i:i + n]
        positions[ngram].append(i)

    # 6. Return only n-grams that occur at least twice.
    return {
        ngram: indices
        for ngram, indices in positions.items()
        if len(indices) >= 2
    }


def calculate_ngram_distances(
    repeated_ngrams: dict[str, list[int]]
) -> dict[str, list[int]]:
    """
    Calculate distances between consecutive occurrences of repeated n-grams.

    Args:
        repeated_ngrams: Dictionary mapping n-grams to their occurrence
            positions in the normalized ciphertext.

    Returns:
        Dictionary mapping each n-gram to a list of consecutive distances.
    """
    if not isinstance(repeated_ngrams, dict):
        raise TypeError("repeated_ngrams must be a dictionary")

    distances = {}

    for ngram, positions in repeated_ngrams.items():
        if not isinstance(ngram, str):
            raise TypeError("n-gram keys must be strings")

        if not isinstance(positions, list):
            raise TypeError("positions must be lists")

        if len(positions) < 2:
            raise ValueError("each n-gram must have at least two positions")

        # Positions must be non-negative integers, excluding bool.
        for position in positions:
            if isinstance(position, bool) or not isinstance(position, int):
                raise TypeError("positions must contain integers")

            if position < 0:
                raise ValueError("positions must be non-negative")

        # Positions must be strictly increasing.
        if any(
            positions[i] >= positions[i + 1]
            for i in range(len(positions) - 1)
        ):
            raise ValueError("positions must be strictly increasing")

        # Calculate distances between consecutive occurrences.
        distances[ngram] = [
            positions[i + 1] - positions[i]
            for i in range(len(positions) - 1)
        ]

    return distances


def calculate_ngram_gcds(
    ngram_distances: dict[str, list[int]]
) -> dict[str, int]:
    """
    Calculate the GCD of distances for each repeated n-gram.

    Args:
        ngram_distances: Dictionary mapping n-grams to their
            consecutive occurrence distances.

    Returns:
        Dictionary mapping each n-gram to its GCD.
    """
    if not isinstance(ngram_distances, dict):
        raise TypeError("ngram_distances must be a dictionary")

    gcd_results = {}

    for ngram, distances in ngram_distances.items():
        if not isinstance(ngram, str):
            raise TypeError("n-gram keys must be strings")

        if not isinstance(distances, list):
            raise TypeError("distances must be lists")

        if not distances:
            raise ValueError("each n-gram must have at least one distance")

        for distance in distances:
            if isinstance(distance, bool) or not isinstance(distance, int):
                raise TypeError("distances must contain integers")

            if distance <= 0:
                raise ValueError("distances must be positive")

        # Calculate the GCD of all distances belonging to this n-gram.
        result = distances[0]

        for distance in distances[1:]:
            result = gcd(result, distance)

        gcd_results[ngram] = result

    return gcd_results
