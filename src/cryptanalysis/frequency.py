
from collections import Counter


def _extract_valid_letters(text: str) -> str:
    """
    Extract valid English ASCII letters (A-Z) from input text.

    The function ignores spaces, punctuation, digits,
    and all non-ASCII alphabetic characters.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    return "".join(
        char.upper()
        for char in text
        if ("A" <= char <= "Z") or ("a" <= char <= "z")
    )


def count_frequencies(text: str) -> dict[str, int]:
    """
    Count the occurrences of each valid English letter.

    Args:
        text: Input text.

    Returns:
        Dictionary mapping each occurring letter to its count.
    """
    letters = _extract_valid_letters(text)

    # Counter counts the occurrences of each character.
    counts = Counter(letters)

    # Return keys in alphabetical order for consistent results.
    return dict(sorted(counts.items()))


def calculate_frequencies(text: str) -> dict[str, float]:
    """
    Calculate the relative frequency of each valid English letter.

    Args:
        text: Input text.

    Returns:
        Dictionary mapping each occurring letter to its relative frequency.
        The sum of frequencies is 1 when at least one valid letter exists.
    """
    counts = count_frequencies(text)
    total = sum(counts.values())

    if total == 0:
        return {}

    return {
        letter: count / total
        for letter, count in counts.items()
    }


def rank_frequencies(text: str) -> list[tuple[str, float]]:
    """
    Rank letters by relative frequency in descending order.

    When two letters have the same frequency, alphabetical order
    is used as the tie-breaker.

    Args:
        text: Input text.

    Returns:
        List of (letter, relative_frequency) tuples.
    """
    frequencies = calculate_frequencies(text)

    return sorted(
        frequencies.items(),
        key=lambda item: (-item[1], item[0])
    )
