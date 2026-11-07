"""Unit tests for classical substitution ciphers."""

import pytest

from src.classical.substitution import (
    multiplicative_decrypt,
    multiplicative_encrypt,
    shift_decrypt,
    shift_encrypt,
)


class TestShiftEncrypt:
    @pytest.mark.parametrize(
        ("plaintext", "key", "expected"),
        [
            ("ATTACK", 3, "DWWDFN"),
            ("HELLO", 3, "KHOOR"),
            ("Hello, World!", 3, "Khoor, Zruog!"),
            ("XYZ", 3, "ABC"),
            ("abc", 3, "def"),
            ("A a Z z", 1, "B b A a"),
            ("ATTACK", 0, "ATTACK"),
            ("ATTACK", 26, "ATTACK"),
            ("ATTACK", 29, "DWWDFN"),
            ("ABC", -1, "ZAB"),
            ("ABC", -27, "ZAB"),
            ("café, Đẹp! 123", 2, "eché, Đẹr! 123"),
            ("", 5, ""),
        ],
    )
    def test_shift_encrypt(self, plaintext, key, expected):
        assert shift_encrypt(plaintext, key) == expected

    @pytest.mark.parametrize("key", [1.5, "3", True, None])
    def test_rejects_non_integer_key(self, key):
        with pytest.raises(TypeError):
            shift_encrypt("ABC", key)

    @pytest.mark.parametrize("plaintext", [None, 123, b"ABC"])
    def test_rejects_non_string_plaintext(self, plaintext):
        with pytest.raises(TypeError, match="text must be a string"):
            shift_encrypt(plaintext, 3)


class TestShiftDecrypt:
    @pytest.mark.parametrize(
        ("ciphertext", "key", "expected"),
        [
            ("DWWDFN", 3, "ATTACK"),
            ("KHOOR", 3, "HELLO"),
            ("Khoor, Zruog!", 3, "Hello, World!"),
            ("ABC", 3, "XYZ"),
            ("def", 3, "abc"),
            ("B b A a", 1, "A a Z z"),
            ("ATTACK", 0, "ATTACK"),
            ("ATTACK", 26, "ATTACK"),
            ("DWWDFN", 29, "ATTACK"),
            ("ZAB", -1, "ABC"),
            ("ZAB", -27, "ABC"),
            ("eché, Đẹr! 123", 2, "café, Đẹp! 123"),
            ("", 5, ""),
        ],
    )
    def test_shift_decrypt(self, ciphertext, key, expected):
        assert shift_decrypt(ciphertext, key) == expected

    @pytest.mark.parametrize("key", [1.5, "3", True, None])
    def test_rejects_non_integer_key(self, key):
        with pytest.raises(TypeError):
            shift_decrypt("ABC", key)

    @pytest.mark.parametrize("ciphertext", [None, 123, b"ABC"])
    def test_rejects_non_string_ciphertext(self, ciphertext):
        with pytest.raises(TypeError, match="text must be a string"):
            shift_decrypt(ciphertext, 3)


class TestShiftRoundTrip:
    @pytest.mark.parametrize(
        ("plaintext", "key"),
        [
            ("Meet me at 10!", 3),
            ("Attack at dawn.", 13),
            ("Mixed CASE, punctuation... 123", -7),
            ("café and Đặng", 29),
            ("", 0),
        ],
    )
    def test_decrypt_after_encrypt_restores_original(self, plaintext, key):
        ciphertext = shift_encrypt(plaintext, key)
        assert shift_decrypt(ciphertext, key) == plaintext


class TestMultiplicativeEncrypt:
    @pytest.mark.parametrize(
        ("plaintext", "key", "expected"),
        [
            ("HELLO", 5, "JUDDS"),
            ("Hello, World!", 5, "Judds, Gshdp!"),
            ("ABCXYZ", 5, "AFKLQV"),
            ("ATTACK", 1, "ATTACK"),
            ("ATTACK", 3, "AFFAGE"),
            ("abc", 5, "afk"),
            ("A a Z z", 5, "A a V v"),
            ("HELLO", 29, "VMHHQ"),  # 29 mod 26 == 3.
            ("HELLO", 31, "JUDDS"),
            ("ABC", -21, "AFK"),  # -21 mod 26 == 5.
            ("", 5, ""),
            ("café, Đẹp! 123", 5, "kazé, Đẹx! 123"),
        ],
    )
    def test_multiplicative_encrypt(self, plaintext, key, expected):
        assert multiplicative_encrypt(plaintext, key) == expected

    @pytest.mark.parametrize("key", [0, 2, 4, 6, 8, 10, 12, 13, 14, 16, 18, 20, 22, 24, 26])
    def test_rejects_non_invertible_keys(self, key):
        with pytest.raises(ValueError, match="relatively prime to 26"):
            multiplicative_encrypt("ABC", key)

    @pytest.mark.parametrize("key", [1.5, "5", True, None])
    def test_rejects_non_integer_key(self, key):
        with pytest.raises(TypeError):
            multiplicative_encrypt("ABC", key)

    @pytest.mark.parametrize("plaintext", [None, 123, b"ABC"])
    def test_rejects_non_string_plaintext(self, plaintext):
        with pytest.raises(TypeError, match="text must be a string"):
            multiplicative_encrypt(plaintext, 5)


class TestMultiplicativeDecrypt:
    @pytest.mark.parametrize(
        ("ciphertext", "key", "expected"),
        [
            ("JUDDS", 5, "HELLO"),
            ("Judds, Gshdp!", 5, "Hello, World!"),
            ("AFKLQV", 5, "ABCXYZ"),
            ("ATTACK", 1, "ATTACK"),
            ("AFFAGE", 3, "ATTACK"),
            ("afk", 5, "abc"),
            ("A a V v", 5, "A a Z z"),
            ("JUDDS", 31, "HELLO"),
            ("AFK", -21, "ABC"),
            ("", 5, ""),
        ],
    )
    def test_multiplicative_decrypt(self, ciphertext, key, expected):
        assert multiplicative_decrypt(ciphertext, key) == expected

    @pytest.mark.parametrize("key", [0, 2, 4, 6, 8, 10, 12, 13, 14, 16, 18, 20, 22, 24, 26])
    def test_rejects_non_invertible_keys(self, key):
        with pytest.raises(ValueError, match="relatively prime to 26"):
            multiplicative_decrypt("ABC", key)

    @pytest.mark.parametrize("key", [1.5, "5", True, None])
    def test_rejects_non_integer_key(self, key):
        with pytest.raises(TypeError):
            multiplicative_decrypt("ABC", key)

    @pytest.mark.parametrize("ciphertext", [None, 123, b"ABC"])
    def test_rejects_non_string_ciphertext(self, ciphertext):
        with pytest.raises(TypeError, match="text must be a string"):
            multiplicative_decrypt(ciphertext, 5)


class TestMultiplicativeRoundTrip:
    @pytest.mark.parametrize(
        ("plaintext", "key"),
        [
            ("HELLO WORLD", 1),
            ("Attack at dawn!", 3),
            ("Mixed CASE, punctuation... 123", 5),
            ("café and Đặng", 7),
            ("HELLO", 9),
            ("HELLO", 11),
            ("HELLO", 15),
            ("HELLO", 17),
            ("HELLO", 19),
            ("HELLO", 21),
            ("HELLO", 23),
            ("HELLO", 25),
            ("", 5),
        ],
    )
    def test_decrypt_after_encrypt_restores_original(self, plaintext, key):
        ciphertext = multiplicative_encrypt(plaintext, key)
        assert multiplicative_decrypt(ciphertext, key) == plaintext
