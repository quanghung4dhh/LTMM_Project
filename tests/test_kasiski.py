
import pytest

from src.cryptanalysis.kasiski import find_repeated_ngrams


# --------------------------------------------------
# Basic functionality
# --------------------------------------------------

def test_find_repeated_ngrams_basic():
    ciphertext = "ABCXABCYABC"

    result = find_repeated_ngrams(ciphertext, n=3)

    assert result == {"ABC": [0, 4, 8]}


def test_find_repeated_ngrams_case_insensitive():
    ciphertext = "abcXABC"

    result = find_repeated_ngrams(ciphertext, n=3)

    assert result == {"ABC": [0, 4]}


def test_find_repeated_ngrams_with_overlapping_positions():
    ciphertext = "AAAA"

    result = find_repeated_ngrams(ciphertext, n=3)

    assert result == {"AAA": [0, 1]}


def test_find_repeated_ngrams_no_repetition():
    ciphertext = "ABCDEFG"

    result = find_repeated_ngrams(ciphertext, n=3)

    assert result == {}


# --------------------------------------------------
# Input normalization
# --------------------------------------------------

def test_find_repeated_ngrams_empty_string():
    assert find_repeated_ngrams("") == {}


def test_find_repeated_ngrams_n_larger_than_text():
    assert find_repeated_ngrams("ABC", n=4) == {}


def test_find_repeated_ngrams_ignores_punctuation_and_spaces():
    ciphertext = "ABC! ABC?"

    result = find_repeated_ngrams(ciphertext, n=3)

    assert result == {"ABC": [0, 3]}


def test_find_repeated_ngrams_ignores_unicode():
    ciphertext = "ABCéABC"

    result = find_repeated_ngrams(ciphertext, n=3)

    assert result == {"ABC": [0, 3]}


# --------------------------------------------------
# Different n values
# --------------------------------------------------

def test_find_repeated_ngrams_with_n_equal_to_one():
    ciphertext = "ABACA"

    result = find_repeated_ngrams(ciphertext, n=1)

    assert result == {"A": [0, 2, 4]}


def test_find_repeated_ngrams_with_n_equal_to_two():
    ciphertext = "ABAB"

    result = find_repeated_ngrams(ciphertext, n=2)

    assert result == {"AB": [0, 2]}


# --------------------------------------------------
# Invalid n
# --------------------------------------------------

@pytest.mark.parametrize("n", [0, -1, -5])
def test_find_repeated_ngrams_invalid_n_value(n):
    with pytest.raises(ValueError):
        find_repeated_ngrams("ABCABC", n=n)


@pytest.mark.parametrize("n", [2.5, "3", None, True, False])
def test_find_repeated_ngrams_invalid_n_type(n):
    with pytest.raises(TypeError):
        find_repeated_ngrams("ABCABC", n=n)


# --------------------------------------------------
# Invalid ciphertext
# --------------------------------------------------

@pytest.mark.parametrize("ciphertext", [None, 123, [], {}])
def test_find_repeated_ngrams_invalid_ciphertext_type(ciphertext):
    with pytest.raises(TypeError):
        find_repeated_ngrams(ciphertext)
