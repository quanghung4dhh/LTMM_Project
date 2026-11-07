"""Unit tests for the repeating-key Vigenere cipher."""

import pytest

from src.classical.vigenere import vigenere_decrypt, vigenere_encrypt


class TestVigenereEncrypt:
    @pytest.mark.parametrize(
        ("plaintext", "key", "expected"),
        [
            ("ATTACKATDAWN", "LEMON", "LXFOPVEFRNHR"),
            ("Hello, World!", "KEY", "Rijvs, Uyvjn!"),
            ("HELLO", "A", "HELLO"),
            ("HELLO", "B", "IFMMP"),
            ("ABCXYZ", "BC", "BDDZZB"),
            ("abc", "key", "kfa"),
            ("A a Z z", "BC", "B c A b"),
            ("Meet me at 10!", "LEMON", "Xiqh zp ef 10!"),
            ("", "LEMON", ""),
            ("123 !? -", "LEMON", "123 !? -"),
            ("café, Đẹp! 123", "KEY", "medé, Đẹz! 123"),
        ],
    )
    def test_encrypt_known_cases(self, plaintext, key, expected):
        assert vigenere_encrypt(plaintext, key) == expected

    @pytest.mark.parametrize("key", ["", "LE MON", "KEY123", "HELLO!", "éclair"])
    def test_rejects_invalid_key(self, key):
        with pytest.raises(ValueError):
            vigenere_encrypt("ABC", key)

    @pytest.mark.parametrize("key", [None, 123, b"KEY"])
    def test_rejects_non_string_key(self, key):
        with pytest.raises(TypeError, match="key must be a string"):
            vigenere_encrypt("ABC", key)

    @pytest.mark.parametrize("plaintext", [None, 123, b"ABC"])
    def test_rejects_non_string_plaintext(self, plaintext):
        with pytest.raises(TypeError, match="text must be a string"):
            vigenere_encrypt(plaintext, "KEY")


class TestVigenereDecrypt:
    @pytest.mark.parametrize(
        ("ciphertext", "key", "expected"),
        [
            ("LXFOPVEFRNHR", "LEMON", "ATTACKATDAWN"),
            ("Rijvs, Uyvjn!", "KEY", "Hello, World!"),
            ("HELLO", "A", "HELLO"),
            ("IFMMP", "B", "HELLO"),
            ("BDDZZB", "BC", "ABCXYZ"),
            ("kfa", "KEY", "abc"),
            ("B c A b", "BC", "A a Z z"),
            ("Xiqh zp ef 10!", "LEMON", "Meet me at 10!"),
            ("", "LEMON", ""),
            ("123 !? -", "LEMON", "123 !? -"),
            ("medé, Đẹz! 123", "KEY", "café, Đẹp! 123"),
        ],
    )
    def test_decrypt_known_cases(self, ciphertext, key, expected):
        assert vigenere_decrypt(ciphertext, key) == expected

    @pytest.mark.parametrize("key", ["", "LE MON", "KEY123", "HELLO!", "éclair"])
    def test_rejects_invalid_key(self, key):
        with pytest.raises(ValueError):
            vigenere_decrypt("ABC", key)

    @pytest.mark.parametrize("key", [None, 123, b"KEY"])
    def test_rejects_non_string_key(self, key):
        with pytest.raises(TypeError, match="key must be a string"):
            vigenere_decrypt("ABC", key)

    @pytest.mark.parametrize("ciphertext", [None, 123, b"ABC"])
    def test_rejects_non_string_ciphertext(self, ciphertext):
        with pytest.raises(TypeError, match="text must be a string"):
            vigenere_decrypt(ciphertext, "KEY")


class TestVigenereRoundTrip:
    @pytest.mark.parametrize(
        ("plaintext", "key"),
        [
            ("ATTACK AT DAWN", "LEMON"),
            ("Mixed CASE, punctuation... 123", "CRYPTO"),
            ("café and Đặng", "KEY"),
            ("A", "LONGERKEY"),
            ("", "A"),
            ("Only punctuation: !? 123", "ABC"),
        ],
    )
    def test_decrypt_after_encrypt_restores_original(self, plaintext, key):
        ciphertext = vigenere_encrypt(plaintext, key)
        assert vigenere_decrypt(ciphertext, key) == plaintext


class TestVigenereKeyProgression:
    def test_punctuation_and_spaces_do_not_consume_key(self):
        # The two A letters use B and C respectively, even though punctuation
        # and whitespace occur between them.
        assert vigenere_encrypt("A-A A", "BC") == "B-C B"

    def test_non_ascii_letters_do_not_consume_key(self):
        assert vigenere_encrypt("AéA", "BC") == "BéC"

    def test_key_restarts_after_its_last_character(self):
        assert vigenere_encrypt("AAAAA", "BC") == "BCBCB"
