
"""Unit tests for classical transposition ciphers."""

import pytest

from src.classical.transposition import (
    rail_fence_encrypt,
    rail_fence_decrypt,
    columnar_encrypt,
    columnar_decrypt,
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


class TestColumnarEncrypt:

    @pytest.mark.parametrize(
        ("plaintext", "key", "expected"),
        [
            (
                "ATTACKATDAWN",
                [3, 1, 4, 2],
                "TAWACDATNTKA",
            ),
            (
                "HELLOWORLD",
                [3, 1, 4, 2],
                "LOHOLLREWD",
            ),
            (
                "CRYPTOGRAPHY",
                [2, 4, 1, 3],
                "ROPPRYCTAYGH",
            ),
            (
                "WELCOMETOTHEWORLD",
                [3, 2, 6, 1, 5, 4],
                "LORETOMEWEWOHDCTL",
            ),
            (
                "ABCDEFGH",
                [1, 2, 3, 4],
                "AEBFCGDH",
            ),
            (
                "ABC",
                [2, 4, 1, 3],
                "BAC",
            ),
            (
                "",
                [3, 1, 4, 2],
                "",
            ),
            (
                "A",
                [1],
                "A",
            ),
            (
                "A,éB!",
                [2, 1],
                ",BAé!",
            ),
        ],
    )
    def test_encrypt_known_cases(self, plaintext, key, expected):
        assert columnar_encrypt(plaintext, key) == expected

    @pytest.mark.parametrize(
        "key",
        [
            [],
            [1, 1],
            [0, 1],
            [1, 3],
        ],
    )
    def test_rejects_invalid_permutations(self, key):
        with pytest.raises(ValueError):
            columnar_encrypt("ATTACKATDAWN", key)

    @pytest.mark.parametrize(
        "key",
        [
            None,
            123,
            "123",
            [True, 2],
            [1, 2.5],
        ],
    )
    def test_rejects_invalid_key_types(self, key):
        with pytest.raises(TypeError):
            columnar_encrypt("ATTACKATDAWN", key)

    @pytest.mark.parametrize(
        "plaintext",
        [
            None,
            123,
            b"ATTACKATDAWN",
        ],
    )
    def test_rejects_non_string_plaintext(self, plaintext):
        with pytest.raises(TypeError):
            columnar_encrypt(plaintext, [3, 1, 4, 2])


class TestColumnarDecrypt:

    @pytest.mark.parametrize(
        ("ciphertext", "key", "expected"),
        [
            (
                "TAWACDATNTKA",
                [3, 1, 4, 2],
                "ATTACKATDAWN",
            ),
            (
                "LOHOLLREWD",
                [3, 1, 4, 2],
                "HELLOWORLD",
            ),
            (
                "ROPPRYCTAYGH",
                [2, 4, 1, 3],
                "CRYPTOGRAPHY",
            ),
            (
                "LORETOMEWEWOHDCTL",
                [3, 2, 6, 1, 5, 4],
                "WELCOMETOTHEWORLD",
            ),
            (
                "AEBFCGDH",
                [1, 2, 3, 4],
                "ABCDEFGH",
            ),
            (
                "BAC",
                [2, 4, 1, 3],
                "ABC",
            ),
            (
                "",
                [3, 1, 4, 2],
                "",
            ),
            (
                "A",
                [1],
                "A",
            ),
            (
                ",BAé!",
                [2, 1],
                "A,éB!",
            ),
        ],
    )
    def test_decrypt_known_cases(self, ciphertext, key, expected):
        assert columnar_decrypt(ciphertext, key) == expected

    @pytest.mark.parametrize(
        "key",
        [
            [],
            [1, 1],
            [0, 1],
            [1, 3],
        ],
    )
    def test_rejects_invalid_permutations(self, key):
        with pytest.raises(ValueError):
            columnar_decrypt("TAWACDATNTKA", key)

    @pytest.mark.parametrize(
        "key",
        [
            None,
            123,
            "123",
            [True, 2],
            [1, 2.5],
        ],
    )
    def test_rejects_invalid_key_types(self, key):
        with pytest.raises(TypeError):
            columnar_decrypt("TAWACDATNTKA", key)

    @pytest.mark.parametrize(
        "ciphertext",
        [
            None,
            123,
            b"ABC",
        ],
    )
    def test_rejects_non_string_ciphertext(self, ciphertext):
        with pytest.raises(TypeError):
            columnar_decrypt(ciphertext, [3, 1, 4, 2])


class TestColumnarRoundTrip:

    @pytest.mark.parametrize(
        ("plaintext", "key"),
        [
            ("ATTACKATDAWN", [3, 1, 4, 2]),
            ("HELLOWORLD", [3, 1, 4, 2]),
            ("CRYPTOGRAPHY", [2, 4, 1, 3]),
            ("WELCOMETOTHEWORLD", [3, 2, 6, 1, 5, 4]),
            ("ABCDEFGH", [1, 2, 3, 4]),
            ("ABC", [2, 4, 1, 3]),
            ("", [3, 1, 4, 2]),
            ("A", [1]),
            ("A,éB!", [2, 1]),
        ],
    )
    def test_decrypt_after_encrypt_restores_original(
        self,
        plaintext,
        key,
    ):
        ciphertext = columnar_encrypt(plaintext, key)
        recovered = columnar_decrypt(ciphertext, key)

        assert recovered == plaintext
