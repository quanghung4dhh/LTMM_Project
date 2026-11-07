"""Unit tests for the Affine cipher implementation."""

import pytest

from src.classical.substitution import (
    affine_decrypt,
    affine_encrypt,
    multiplicative_encrypt,
    shift_encrypt,
)


class TestAffineEncrypt:
    @pytest.mark.parametrize(
        ("plaintext", "a", "b", "expected"),
        [
            ("AFFINECIPHER", 5, 8, "IHHWVCSWFRCP"),
            ("HELLO", 5, 8, "RCLLA"),
            ("Hello, World!", 5, 8, "Rclla, Oaplx!"),
            ("ABCXYZ", 1, 3, "DEFABC"),
            ("ATTACK", 1, 0, "ATTACK"),
            ("ABC", 3, 0, "ADG"),
            ("abc", 5, 8, "ins"),
            ("A a Z z", 5, 8, "I i D d"),
            ("HELLO", 31, 34, "RCLLA"),  # 31 mod 26 = 5; 34 mod 26 = 8.
            ("HELLO", -21, -18, "RCLLA"),
            ("HELLO", 5, -18, "RCLLA"),
            ("", 5, 8, ""),
            ("café, Đẹp! 123", 5, 8, "sihé, Đẹf! 123"),
        ],
    )
    def test_affine_encrypt(self, plaintext, a, b, expected):
        assert affine_encrypt(plaintext, a, b) == expected

    @pytest.mark.parametrize("a", [0, 2, 4, 6, 8, 10, 12, 13, 14, 16, 18, 20, 22, 24, 26])
    def test_rejects_non_invertible_a(self, a):
        with pytest.raises(ValueError, match="relatively prime to 26"):
            affine_encrypt("ABC", a, 7)

    @pytest.mark.parametrize("a", [1.5, "5", True, None])
    def test_rejects_invalid_a_type(self, a):
        with pytest.raises(TypeError):
            affine_encrypt("ABC", a, 8)

    @pytest.mark.parametrize("b", [1.5, "8", True, None])
    def test_rejects_invalid_b_type(self, b):
        with pytest.raises(TypeError):
            affine_encrypt("ABC", 5, b)

    @pytest.mark.parametrize("plaintext", [None, 123, b"ABC"])
    def test_rejects_non_string_plaintext(self, plaintext):
        with pytest.raises(TypeError, match="text must be a string"):
            affine_encrypt(plaintext, 5, 8)


class TestAffineDecrypt:
    @pytest.mark.parametrize(
        ("ciphertext", "a", "b", "expected"),
        [
            ("IHHWVCSWFRCP", 5, 8, "AFFINECIPHER"),
            ("RCLLA", 5, 8, "HELLO"),
            ("Rclla, Oaplx!", 5, 8, "Hello, World!"),
            ("DEFABC", 1, 3, "ABCXYZ"),
            ("ATTACK", 1, 0, "ATTACK"),
            ("ADG", 3, 0, "ABC"),
            ("rclla", 5, 8, "hello"),
            ("I i D d", 5, 8, "A a Z z"),
            ("sihé, Đẹf! 123", 5, 8, "café, Đẹp! 123"),
            ("RCLLA", 31, 34, "HELLO"),
            ("RCLLA", -21, -18, "HELLO"),
            ("", 5, 8, ""),
        ],
    )
    def test_affine_decrypt(self, ciphertext, a, b, expected):
        assert affine_decrypt(ciphertext, a, b) == expected

    @pytest.mark.parametrize("a", [0, 2, 4, 6, 8, 10, 12, 13, 14, 16, 18, 20, 22, 24, 26])
    def test_rejects_non_invertible_a(self, a):
        with pytest.raises(ValueError, match="relatively prime to 26"):
            affine_decrypt("ABC", a, 7)

    @pytest.mark.parametrize("a", [1.5, "5", True, None])
    def test_rejects_invalid_a_type(self, a):
        with pytest.raises(TypeError):
            affine_decrypt("ABC", a, 8)

    @pytest.mark.parametrize("b", [1.5, "8", True, None])
    def test_rejects_invalid_b_type(self, b):
        with pytest.raises(TypeError):
            affine_decrypt("ABC", 5, b)

    @pytest.mark.parametrize("ciphertext", [None, 123, b"ABC"])
    def test_rejects_non_string_ciphertext(self, ciphertext):
        with pytest.raises(TypeError, match="text must be a string"):
            affine_decrypt(ciphertext, 5, 8)


class TestAffineRoundTrip:
    @pytest.mark.parametrize(
        ("plaintext", "a", "b"),
        [
            ("Meet me at 10!", 5, 8),
            ("Attack at dawn.", 7, 3),
            ("Mixed CASE, punctuation... 123", 11, 19),
            ("café and Đặng", 25, 7),
            ("AFFINECIPHER", 1, 25),
            ("HELLO", -21, 34),
            ("", 5, 0),
        ],
    )
    def test_decrypt_after_encrypt_restores_original(self, plaintext, a, b):
        ciphertext = affine_encrypt(plaintext, a, b)
        assert affine_decrypt(ciphertext, a, b) == plaintext


class TestAffineKeySpace:
    def test_all_12_valid_multiplicative_parameters_round_trip(self):
        valid_a_values = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        plaintext = "Affine cipher test!"

        for a in valid_a_values:
            for b in range(26):
                ciphertext = affine_encrypt(plaintext, a, b)
                assert affine_decrypt(ciphertext, a, b) == plaintext


class TestAffineRelationships:
    def test_affine_with_a_equal_to_one_is_shift(self):
        plaintext = "Affine becomes Shift! 123"
        for b in range(-30, 31):
            assert affine_encrypt(plaintext, 1, b) == shift_encrypt(plaintext, b)

    def test_affine_with_b_equal_to_zero_is_multiplicative(self):
        plaintext = "Affine becomes Multiplicative! 123"
        valid_a_values = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        for a in valid_a_values:
            assert affine_encrypt(plaintext, a, 0) == multiplicative_encrypt(plaintext, a)
