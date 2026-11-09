
"""Unit tests for classical transposition ciphers."""

import pytest

from src.classical.transposition import rail_fence_encrypt


class TestRailFenceEncrypt:

    @pytest.mark.parametrize(
        ("plaintext", "rails", "expected"),
        [
            ("WEAREDISCOVERED", 3, "WECRERDSOEEAIVD"),
            ("HELLOWORLD", 2, "HLOOLELWRD"),
            ("HELLOWORLD", 3, "HOLELWRDLO"),
            ("HELLO", 1, "HELLO"),
            ("ABC", 5, "ABC"),
            ("ABC", 3, "ABC"),
            ("", 3, ""),
            ("A", 3, "A"),
            ("A,éB!", 2, "Aé!,B"),
            ("Hello, World!", 3, "Hoo!el,Wrdl l"),
        ],
    )
    def test_encrypt_known_cases(self, plaintext, rails, expected):
        assert rail_fence_encrypt(plaintext, rails) == expected

    @pytest.mark.parametrize("rails", [0, -1])
    def test_rejects_non_positive_rails(self, rails):
        with pytest.raises(ValueError):
            rail_fence_encrypt("ABC", rails)

    @pytest.mark.parametrize(
        "rails",
        [True, False, 1.5, "3", None],
    )
    def test_rejects_non_integer_rails(self, rails):
        with pytest.raises(TypeError):
            rail_fence_encrypt("ABC", rails)

    @pytest.mark.parametrize(
        "plaintext",
        [None, 123, b"ABC"],
    )
    def test_rejects_non_string_plaintext(self, plaintext):
        with pytest.raises(TypeError):
            rail_fence_encrypt(plaintext, 3)
