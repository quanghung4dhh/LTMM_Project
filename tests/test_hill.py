"""Unit tests for the Hill cipher implementation."""

import pytest

from classical.hill import hill_decrypt, hill_encrypt


KEY_2X2 = [[3, 3], [2, 5]]
KEY_3X3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]


class TestHillEncrypt:
    @pytest.mark.parametrize(
        ("plaintext", "key", "expected_ciphertext", "expected_padding"),
        [
            ("HELP", KEY_2X2, "HIAT", 0),
            ("ACT", KEY_3X3, "POH", 0),
            ("HELLO", KEY_2X2, "HIOZHN", 1),
            ("HELLO!", KEY_2X2, "HIOZH!N", 1),
            ("hello", KEY_2X2, "hiozhN", 1),
            ("A", KEY_2X2, "RL", 1),
            ("", KEY_2X2, "", 0),
            ("123 !?", KEY_2X2, "123 !?", 0),
        ],
    )
    def test_known_cases(self, plaintext, key, expected_ciphertext, expected_padding):
        ciphertext, padding = hill_encrypt(plaintext, key)
        assert ciphertext == expected_ciphertext
        assert padding == expected_padding

    def test_preserves_punctuation_and_case(self):
        ciphertext, padding = hill_encrypt("He, lp!", KEY_2X2)
        assert hill_decrypt(ciphertext, KEY_2X2,
                            padding_length=padding) == "He, lp!"

    def test_preserves_unicode_and_digits(self):
        plaintext = "café, Đẹp! 123"
        ciphertext, padding = hill_encrypt(plaintext, KEY_2X2)
        assert hill_decrypt(ciphertext, KEY_2X2,
                            padding_length=padding) == plaintext

    def test_accepts_negative_and_large_matrix_entries(self):
        equivalent_key = [[29, 29], [-24, 5]]
        ciphertext, padding = hill_encrypt("HELP", equivalent_key)
        assert ciphertext == "HIAT"
        assert padding == 0

    def test_does_not_mutate_key_matrix(self):
        key = [[3, 3], [2, 5]]
        before = [row[:] for row in key]
        hill_encrypt("HELP", key)
        assert key == before


class TestHillDecrypt:
    @pytest.mark.parametrize(
        ("ciphertext", "key", "padding", "expected"),
        [
            ("HIAT", KEY_2X2, 0, "HELP"),
            ("POH", KEY_3X3, 0, "ACT"),
            ("HIOZHN", KEY_2X2, 1, "HELLO"),
            ("HIOZH!N", KEY_2X2, 1, "HELLO!"),
            ("hiozhN", KEY_2X2, 1, "hello"),
            ("RL", KEY_2X2, 1, "A"),
            ("", KEY_2X2, 0, ""),
        ],
    )
    def test_known_cases(self, ciphertext, key, padding, expected):
        assert hill_decrypt(
            ciphertext, key, padding_length=padding
        ) == expected

    def test_literal_x_at_end_is_not_removed_without_metadata(self):
        ciphertext, padding = hill_encrypt("AX", KEY_2X2)
        assert padding == 0
        assert hill_decrypt(ciphertext, KEY_2X2) == "AX"

    def test_original_x_and_padding_x_are_distinguished(self):
        ciphertext, padding = hill_encrypt("AXA", KEY_2X2)
        assert padding == 1
        assert hill_decrypt(
            ciphertext, KEY_2X2, padding_length=padding
        ) == "AXA"

    def test_rejects_wrong_padding_length_when_suffix_is_not_x(self):
        ciphertext, padding = hill_encrypt("HELP", KEY_2X2)
        assert padding == 0
        with pytest.raises(ValueError, match="expected X padding"):
            hill_decrypt(ciphertext, KEY_2X2, padding_length=1)

    def test_rejects_ciphertext_letter_count_not_divisible_by_block_size(self):
        with pytest.raises(ValueError, match="divisible"):
            hill_decrypt("ABC", KEY_2X2)


class TestHillKeyValidation:
    @pytest.mark.parametrize(
        "invalid_key",
        [
            [],
            [[1, 2, 3], [4, 5, 6]],
            [[1, 2], [3]],
            [[1]],
            [[2, 0], [0, 1]],
            [[13, 0], [0, 1]],
            [[1, 2], [2, 4]],
        ],
    )
    def test_rejects_invalid_or_non_invertible_key(self, invalid_key):
        with pytest.raises(ValueError):
            hill_encrypt("HELP", invalid_key)

    @pytest.mark.parametrize(
        "invalid_key",
        [
            [[1.5, 2], [3, 4]],
            [[True, 2], [3, 4]],
            "not-a-matrix",
            None,
        ],
    )
    def test_rejects_invalid_key_types(self, invalid_key):
        with pytest.raises(TypeError):
            hill_encrypt("HELP", invalid_key)


class TestHillInputValidation:
    @pytest.mark.parametrize("plaintext", [None, 123, b"HELP"])
    def test_encrypt_rejects_non_string_plaintext(self, plaintext):
        with pytest.raises(TypeError, match="plaintext must be a string"):
            hill_encrypt(plaintext, KEY_2X2)

    @pytest.mark.parametrize("ciphertext", [None, 123, b"HIAT"])
    def test_decrypt_rejects_non_string_ciphertext(self, ciphertext):
        with pytest.raises(TypeError, match="ciphertext must be a string"):
            hill_decrypt(ciphertext, KEY_2X2)

    @pytest.mark.parametrize("padding", [True, 1.5, "1", None])
    def test_decrypt_rejects_non_integer_padding_length(self, padding):
        with pytest.raises(TypeError, match="padding_length must be an integer"):
            hill_decrypt("HIAT", KEY_2X2, padding_length=padding)

    @pytest.mark.parametrize("padding", [-1, 2, 3])
    def test_decrypt_rejects_padding_out_of_range(self, padding):
        with pytest.raises(ValueError, match="padding_length must be between"):
            hill_decrypt("HIAT", KEY_2X2, padding_length=padding)


class TestHillRoundTrip:
    @pytest.mark.parametrize(
        ("plaintext", "key"),
        [
            ("HELP", KEY_2X2),
            ("HELLO", KEY_2X2),
            ("HELLO!", KEY_2X2),
            ("Attack at dawn!", KEY_2X2),
            ("Mixed CASE, punctuation... 123", KEY_2X2),
            ("café and Đặng", KEY_2X2),
            ("AXA", KEY_2X2),
            ("ACT", KEY_3X3),
            ("ATTACKATDAWN", KEY_3X3),
            ("", KEY_2X2),
            ("Only punctuation: !? 123", KEY_3X3),
        ],
    )
    def test_encrypt_then_decrypt_restores_original(self, plaintext, key):
        ciphertext, padding = hill_encrypt(plaintext, key)
        restored = hill_decrypt(
            ciphertext, key, padding_length=padding
        )
        assert restored == plaintext
