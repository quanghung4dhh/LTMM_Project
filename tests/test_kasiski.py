
from src.cryptanalysis.kasiski import calculate_ngram_distances
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


def test_calculate_ngram_distances_basic():
    repeated_ngrams = {
        "ABC": [0, 4, 8],
        "XYZ": [2, 8, 14],
        "DEF": [1, 10],
    }

    result = calculate_ngram_distances(repeated_ngrams)

    assert result == {
        "ABC": [4, 4],
        "XYZ": [6, 6],
        "DEF": [9],
    }


def test_calculate_ngram_distances_two_occurrences():
    result = calculate_ngram_distances({"ABC": [3, 10]})

    assert result == {"ABC": [7]}


def test_calculate_ngram_distances_empty_input():
    assert calculate_ngram_distances({}) == {}


def test_calculate_ngram_distances_large_positions():
    result = calculate_ngram_distances({
        "ABC": [100, 250, 500]
    })

    assert result == {"ABC": [150, 250]}


def test_calculate_ngram_distances_does_not_modify_input():
    repeated_ngrams = {"ABC": [0, 5, 10]}
    original = {"ABC": [0, 5, 10]}

    calculate_ngram_distances(repeated_ngrams)

    assert repeated_ngrams == original


@pytest.mark.parametrize(
    "invalid_input",
    [None, [], "ABC", 123]
)
def test_calculate_ngram_distances_invalid_input_type(invalid_input):
    with pytest.raises(TypeError):
        calculate_ngram_distances(invalid_input)


def test_calculate_ngram_distances_invalid_positions_length():
    with pytest.raises(ValueError):
        calculate_ngram_distances({"ABC": [5]})


@pytest.mark.parametrize(
    "positions",
    [[0, 0], [5, 3], [0, -1]]
)
def test_calculate_ngram_distances_invalid_position_values(positions):
    with pytest.raises(ValueError):
        calculate_ngram_distances({"ABC": positions})


@pytest.mark.parametrize(
    "positions",
    [[0, 5.5], [0, "5"], [0, True]]
)
def test_calculate_ngram_distances_invalid_position_types(positions):
    with pytest.raises(TypeError):
        calculate_ngram_distances({"ABC": positions})
