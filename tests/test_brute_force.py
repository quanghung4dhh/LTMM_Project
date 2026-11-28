
from src.cryptanalysis.brute_force import brute_force_affine
from src.classical.substitution import affine_encrypt
from src.cryptanalysis.brute_force import (
    brute_force_caesar,
    brute_force_affine,
)
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


def test_affine_returns_312_candidates():
    """Affine brute force must return exactly 312 candidates."""
    results = brute_force_affine("HELLO")

    assert len(results) == 312


def test_affine_tries_all_valid_a_keys():
    """Only multiplicative keys coprime to 26 are allowed."""
    results = brute_force_affine("HELLO")

    valid_a = [
        1, 3, 5, 7, 9, 11,
        15, 17, 19, 21, 23, 25
    ]

    tested_a = sorted(set(a for a, b, plaintext in results))

    assert tested_a == valid_a


def test_affine_tries_all_b_keys():
    """Every additive key from 0 to 25 must be tested."""
    results = brute_force_affine("HELLO")

    for a in range(26):
        if a in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
            tested_b = [
                b for current_a, b, plaintext in results
                if current_a == a
            ]

            assert tested_b == list(range(26))


def test_affine_finds_correct_plaintext():
    """Brute force must recover plaintext using the correct key."""
    plaintext = "HELLO WORLD"
    a, b = 5, 8

    ciphertext = affine_encrypt(plaintext, a, b)
    results = brute_force_affine(ciphertext)

    assert (a, b, plaintext) in results


def test_affine_preserves_case_and_punctuation():
    """Letter case, punctuation, and digits must be preserved."""
    plaintext = "Hello, World! 123"
    ciphertext = affine_encrypt(plaintext, 5, 8)

    results = brute_force_affine(ciphertext)

    assert (5, 8, plaintext) in results


def test_affine_empty_string():
    """An empty ciphertext must produce 312 empty candidates."""
    results = brute_force_affine("")

    assert len(results) == 312
    assert all(plaintext == "" for a, b, plaintext in results)


@pytest.mark.parametrize(
    "invalid_input",
    [None, 123, ["A", "B"]]
)
def test_affine_rejects_non_string(invalid_input):
    """Non-string inputs must raise TypeError."""
    with pytest.raises(TypeError):
        brute_force_affine(invalid_input)


def test_affine_key_pairs_are_unique():
    """Every candidate must have a unique key pair."""
    results = brute_force_affine("HELLO")

    key_pairs = [
        (a, b) for a, b, plaintext in results
    ]

    assert len(key_pairs) == len(set(key_pairs))
