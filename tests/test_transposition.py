
"""Unit tests for classical transposition ciphers."""

import pytest

from src.classical.transposition import (
    rail_fence_encrypt,
    rail_fence_decrypt,
)


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


class TestRailFenceDecrypt:

    @pytest.mark.parametrize(
        ("ciphertext", "rails", "expected"),
        [
            (
                "WECRERDSOEEAIVD",
                3,
                "WEAREDISCOVERED",
            ),
            (
                "HLOOLELWRD",
                2,
                "HELLOWORLD",
            ),
            (
                "HOLELWRDLO",
                3,
                "HELLOWORLD",
            ),
            (
                "HELLO",
                1,
                "HELLO",
            ),
            (
                "ABC",
                5,
                "ABC",
            ),
            (
                "",
                3,
                "",
            ),
            (
                "A",
                3,
                "A",
            ),
            (
                "Aé!,B",
                2,
                "A,éB!",
            ),
            (
                "Hoo!el,Wrdl l",
                3,
                "Hello, World!",
            ),
        ],
    )
    def test_decrypt_known_cases(self, ciphertext, rails, expected):
        assert rail_fence_decrypt(ciphertext, rails) == expected

    @pytest.mark.parametrize("rails", [0, -1])
    def test_rejects_non_positive_rails(self, rails):
        with pytest.raises(ValueError):
            rail_fence_decrypt("ABC", rails)

    @pytest.mark.parametrize(
        "rails",
        [True, False, 1.5, "3", None],
    )
    def test_rejects_non_integer_rails(self, rails):
        with pytest.raises(TypeError):
            rail_fence_decrypt("ABC", rails)

    @pytest.mark.parametrize(
        "ciphertext",
        [None, 123, b"ABC"],
    )
    def test_rejects_non_string_ciphertext(self, ciphertext):
        with pytest.raises(TypeError):
            rail_fence_decrypt(ciphertext, 3)


class TestRailFenceRoundTrip:

    @pytest.mark.parametrize(
        ("plaintext", "rails"),
        [
            ("WEAREDISCOVERED", 3),
            ("HELLOWORLD", 2),
            ("HELLOWORLD", 3),
            ("CRYPTOGRAPHY", 4),
            ("A", 3),
            ("", 3),
            ("Hello, World!", 3),
            ("café và mật mã", 4),
            ("A" * 100, 7),
        ],
    )
    def test_decrypt_after_encrypt_restores_original(
        self,
        plaintext,
        rails,
    ):
        ciphertext = rail_fence_encrypt(plaintext, rails)

        recovered = rail_fence_decrypt(ciphertext, rails)

        assert recovered == plaintext
