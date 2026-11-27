
import pytest

from src.cryptanalysis.frequency import (
    count_frequencies,
    calculate_frequencies,
    rank_frequencies,
)


def test_count_frequencies_basic():
    assert count_frequencies("ABABAC") == {
        "A": 3,
        "B": 2,
        "C": 1,
    }


def test_count_frequencies_case_insensitive():
    assert count_frequencies("aAbBcC") == {
        "A": 2,
        "B": 2,
        "C": 2,
    }


def test_count_frequencies_ignores_punctuation_and_digits():
    assert count_frequencies("Hello, World! 123") == {
        "D": 1,
        "E": 1,
        "H": 1,
        "L": 3,
        "O": 2,
        "R": 1,
        "W": 1,
    }


def test_count_frequencies_ignores_unicode():
    assert count_frequencies("Hello é ß") == {
        "E": 1,
        "H": 1,
        "L": 2,
        "O": 1,
    }


@pytest.mark.parametrize("text", ["", "123 !@#", "é ß"])
def test_count_frequencies_empty_valid_input(text):
    assert count_frequencies(text) == {}


def test_calculate_frequencies_basic():
    result = calculate_frequencies("ABABAC")

    assert result["A"] == pytest.approx(0.5)
    assert result["B"] == pytest.approx(1 / 3)
    assert result["C"] == pytest.approx(1 / 6)


def test_calculate_frequencies_sum_to_one():
    result = calculate_frequencies("HELLO WORLD")

    assert sum(result.values()) == pytest.approx(1.0)


def test_calculate_frequencies_empty_input():
    assert calculate_frequencies("") == {}


def test_rank_frequencies_descending():
    assert rank_frequencies("ABABAC") == [
        ("A", 0.5),
        ("B", pytest.approx(1 / 3)),
        ("C", pytest.approx(1 / 6)),
    ]


def test_rank_frequencies_alphabetical_tie_break():
    assert rank_frequencies("CBAD") == [
        ("A", 0.25),
        ("B", 0.25),
        ("C", 0.25),
        ("D", 0.25),
    ]


def test_rank_frequencies_empty_input():
    assert rank_frequencies("") == []


@pytest.mark.parametrize("invalid_input", [None, 123, ["A", "B"]])
def test_frequency_functions_reject_non_string(invalid_input):
    with pytest.raises(TypeError):
        count_frequencies(invalid_input)

    with pytest.raises(TypeError):
        calculate_frequencies(invalid_input)

    with pytest.raises(TypeError):
        rank_frequencies(invalid_input)
