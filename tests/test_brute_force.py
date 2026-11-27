
import pytest

from src.cryptanalysis.brute_force import brute_force_caesar


def test_brute_force_returns_26_candidates():
    """Brute Force must return exactly 26 candidates."""
    results = brute_force_caesar("KHOOR")

    assert len(results) == 26


def test_brute_force_tries_all_keys():
    """All Caesar keys from 0 to 25 must be tested."""
    results = brute_force_caesar("KHOOR")

    keys = [key for key, plaintext in results]

    assert keys == list(range(26))


def test_brute_force_key_zero_returns_original_text():
    """Key 0 must not change the ciphertext."""
    ciphertext = "HELLO WORLD"

    results = brute_force_caesar(ciphertext)

    assert results[0] == (0, ciphertext)


def test_brute_force_finds_correct_caesar_plaintext():
    """Key 3 must recover HELLO WORLD from KHOOR ZRUOG."""
    results = brute_force_caesar("KHOOR ZRUOG")

    assert results[3] == (3, "HELLO WORLD")


def test_brute_force_preserves_letter_case():
    """Original uppercase and lowercase formatting must be preserved."""
    results = brute_force_caesar("Khoor Zruog!")

    assert results[3] == (3, "Hello World!")


def test_brute_force_preserves_punctuation_and_digits():
    """Spaces, punctuation, and digits must remain unchanged."""
    results = brute_force_caesar("Khoor, Zruog! 123")

    assert results[3] == (3, "Hello, World! 123")


def test_brute_force_empty_string():
    """An empty string must produce 26 empty plaintext candidates."""
    results = brute_force_caesar("")

    assert len(results) == 26
    assert all(plaintext == "" for key, plaintext in results)


@pytest.mark.parametrize("invalid_input", [None, 123, ["A", "B"]])
def test_brute_force_rejects_non_string(invalid_input):
    """Non-string inputs must raise TypeError."""
    with pytest.raises(TypeError):
        brute_force_caesar(invalid_input)


def test_brute_force_keys_are_unique():
    """Each candidate must correspond to a unique key."""
    results = brute_force_caesar("HELLO")

    keys = [key for key, plaintext in results]

    assert len(keys) == len(set(keys))
