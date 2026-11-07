"""Unit tests for classical substitution ciphers."""

import pytest

from src.classical.substitution import shift_decrypt, shift_encrypt


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
