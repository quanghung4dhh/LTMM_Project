
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


def rank_key_length_candidates(
    ngram_gcds: dict[str, int],
    min_key_length: int = 2,
    max_key_length: int = 20,
) -> list[tuple[int, int]]:
    """
    Rank possible Vigenere key lengths using GCD results.

    Each n-gram contributes one vote to every candidate key length
    that divides its GCD.

    Args:
        ngram_gcds: Dictionary mapping n-grams to their GCD values.
        min_key_length: Minimum candidate key length.
        max_key_length: Maximum candidate key length.

    Returns:
        A list of (key_length, score) tuples sorted by:
        1. Descending score.
        2. Ascending key length.
    """
    if not isinstance(ngram_gcds, dict):
        raise TypeError("ngram_gcds must be a dictionary")

    if (
        isinstance(min_key_length, bool)
        or not isinstance(min_key_length, int)
    ):
        raise TypeError("min_key_length must be an integer")

    if (
        isinstance(max_key_length, bool)
        or not isinstance(max_key_length, int)
    ):
        raise TypeError("max_key_length must be an integer")

    if min_key_length < 2:
        raise ValueError("min_key_length must be at least 2")

    if max_key_length < min_key_length:
        raise ValueError(
            "max_key_length must be >= min_key_length"
        )

    for ngram, value in ngram_gcds.items():
        if not isinstance(ngram, str):
            raise TypeError("n-gram keys must be strings")

        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("GCD values must be integers")

        if value <= 0:
            raise ValueError("GCD values must be positive")

    # Initialize the score of every candidate key length.
    scores = {
        key_length: 0
        for key_length in range(
            min_key_length,
            max_key_length + 1
        )
    }

    # Each n-gram contributes one vote to each valid divisor.
    for gcd_value in ngram_gcds.values():
        for key_length in scores:
            if gcd_value % key_length == 0:
                scores[key_length] += 1

    # Sort by descending score, then ascending key length.
    return sorted(
        scores.items(),
        key=lambda item: (-item[1], item[0])
    )
