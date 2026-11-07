"""Unit tests for src.classical.common."""

import pytest

from src.classical.common import (
    ALPHABET,
    ALPHABET_SIZE,
    char_to_number,
    is_ascii_letter,
    iter_alpha_positions,
    normalize_alpha_key,
    number_to_char,
)


class TestAlphabetConstants:
    def test_alphabet_definition(self):
        assert ALPHABET == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        assert ALPHABET_SIZE == 26
        assert len(ALPHABET) == ALPHABET_SIZE


class TestIsAsciiLetter:
    @pytest.mark.parametrize("char", ["A", "Z", "a", "z", "M", "m"])
    def test_accepts_ascii_letters(self, char):
        assert is_ascii_letter(char) is True

    @pytest.mark.parametrize("char", ["", "AB", "1", " ", "!", "é", "ơ", "ß"])
    def test_rejects_non_ascii_letters_or_non_single_characters(self, char):
        assert is_ascii_letter(char) is False

    @pytest.mark.parametrize("value", [None, 1, True, b"A"])
    def test_rejects_non_string_input(self, value):
        with pytest.raises(TypeError, match="char must be a string"):
            is_ascii_letter(value)


class TestCharToNumber:
    @pytest.mark.parametrize(
        ("char", "expected"),
        [("A", 0), ("a", 0), ("B", 1), ("H", 7), ("m", 12), ("Z", 25), ("z", 25)],
    )
    def test_converts_letters_to_numbers(self, char, expected):
        assert char_to_number(char) == expected

    @pytest.mark.parametrize("char", ["", "AB", "1", "!", "é", "ơ"])
    def test_rejects_invalid_characters(self, char):
        with pytest.raises(ValueError, match="one ASCII letter"):
            char_to_number(char)

    def test_rejects_non_string_input(self):
        with pytest.raises(TypeError, match="char must be a string"):
            char_to_number(65)


class TestNumberToChar:
    @pytest.mark.parametrize(
        ("number", "expected"),
        [(0, "A"), (1, "B"), (7, "H"), (12, "M"), (25, "Z")],
    )
    def test_converts_numbers_to_uppercase_letters(self, number, expected):
        assert number_to_char(number) == expected

    def test_can_return_lowercase_letter(self):
        assert number_to_char(7, uppercase=False) == "h"

    @pytest.mark.parametrize("number", [-1, 26, 27])
    def test_rejects_values_outside_z26(self, number):
        with pytest.raises(ValueError, match="between 0 and 25"):
            number_to_char(number)

    @pytest.mark.parametrize("number", [1.5, "1", True, None])
    def test_rejects_non_integer_values(self, number):
        with pytest.raises(TypeError, match="number must be an integer"):
            number_to_char(number)

    def test_rejects_non_boolean_uppercase_argument(self):
        with pytest.raises(TypeError, match="uppercase must be a bool"):
            number_to_char(0, uppercase=1)


class TestNormalizeAlphaKey:
    @pytest.mark.parametrize(
        ("key", "expected"),
        [("LEMON", "LEMON"), ("lemon", "LEMON"), ("LeMoN", "LEMON"), ("a", "A")],
    )
    def test_normalizes_valid_key_to_uppercase(self, key, expected):
        assert normalize_alpha_key(key) == expected

    @pytest.mark.parametrize("key", ["", "LE MON", "KEY123", "HELLO!", "éclair", "ß"])
    def test_rejects_invalid_keys(self, key):
        with pytest.raises(ValueError, match="key"):
            normalize_alpha_key(key)

    def test_rejects_non_string_key(self):
        with pytest.raises(TypeError, match="key must be a string"):
            normalize_alpha_key(None)

    def test_error_identifies_invalid_character_position(self):
        with pytest.raises(ValueError, match="position 3"):
            normalize_alpha_key("KEY 123")


class TestIterAlphaPositions:
    def test_yields_only_ascii_letter_positions(self):
        text = "Hi, World! 123"
        assert list(iter_alpha_positions(text)) == [
            (0, "H"),
            (1, "i"),
            (4, "W"),
            (5, "o"),
            (6, "r"),
            (7, "l"),
            (8, "d"),
        ]

    def test_preserves_original_case(self):
        assert list(iter_alpha_positions("aZ-b")) == [
            (0, "a"),
            (1, "Z"),
            (3, "b"),
        ]

    def test_empty_text_returns_no_positions(self):
        assert list(iter_alpha_positions("")) == []

    def test_non_ascii_letters_are_skipped(self):
        assert list(iter_alpha_positions("café-Đẹp")) == [
            (0, "c"),
            (1, "a"),
            (2, "f"),
            (7, "p"),
        ]

    def test_rejects_non_string_text(self):
        with pytest.raises(TypeError, match="text must be a string"):
            list(iter_alpha_positions(None))
