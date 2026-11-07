"""Unit tests for the plaintext-autokey cipher."""

import pytest

from src.classical.autokey import autokey_decrypt, autokey_encrypt


class TestAutokeyEncrypt:
    @pytest.mark.parametrize(
        ("plaintext", "seed_key", "expected"),
        [
            ("ATTACKATDAWN", "QUEEN", "QNXEPKTMDCGN"),
            ("HELLO", "KEY", "RIJSS"),
            ("Hello, World!", "KEY", "Rijss, Hzfhr!"),
            ("AAAAA", "BC", "BCAAA"),
            ("HELLO", "LONGERKEY", "SSYRS"),
            ("A-A A", "BC", "B-C A"),
            ("AéA", "BC", "BéC"),
            ("abc", "key", "kfa"),
            ("", "QUEEN", ""),
            ("123 !? -", "QUEEN", "123 !? -"),
        ],
    )
    def test_encrypt_known_cases(self, plaintext, seed_key, expected):
        assert autokey_encrypt(plaintext, seed_key) == expected

    @pytest.mark.parametrize(
        "seed_key",
        ["", "LE MON", "KEY123", "HELLO!", "éclair", "ß"],
    )
    def test_rejects_invalid_seed_key(self, seed_key):
        with pytest.raises(ValueError):
            autokey_encrypt("ABC", seed_key)

    @pytest.mark.parametrize("seed_key", [None, 123, b"KEY", True])
    def test_rejects_non_string_seed_key(self, seed_key):
        with pytest.raises(TypeError, match="key must be a string"):
            autokey_encrypt("ABC", seed_key)

    @pytest.mark.parametrize("plaintext", [None, 123, b"ABC"])
    def test_rejects_non_string_plaintext(self, plaintext):
        with pytest.raises(TypeError, match="text must be a string"):
            autokey_encrypt(plaintext, "KEY")


class TestAutokeyDecrypt:
    @pytest.mark.parametrize(
        ("ciphertext", "seed_key", "expected"),
        [
            ("QNXEPKTMDCGN", "QUEEN", "ATTACKATDAWN"),
            ("RIJSS", "KEY", "HELLO"),
            ("Rijss, Hzfhr!", "KEY", "Hello, World!"),
            ("BCAAA", "BC", "AAAAA"),
            ("SSYRS", "LONGERKEY", "HELLO"),
            ("B-C A", "BC", "A-A A"),
            ("BéC", "BC", "AéA"),
            ("kfa", "KEY", "abc"),
            ("", "QUEEN", ""),
            ("123 !? -", "QUEEN", "123 !? -"),
        ],
    )
    def test_decrypt_known_cases(self, ciphertext, seed_key, expected):
        assert autokey_decrypt(ciphertext, seed_key) == expected

    @pytest.mark.parametrize(
        "seed_key",
        ["", "LE MON", "KEY123", "HELLO!", "éclair", "ß"],
    )
    def test_rejects_invalid_seed_key(self, seed_key):
        with pytest.raises(ValueError):
            autokey_decrypt("ABC", seed_key)

    @pytest.mark.parametrize("seed_key", [None, 123, b"KEY", True])
    def test_rejects_non_string_seed_key(self, seed_key):
        with pytest.raises(TypeError, match="key must be a string"):
            autokey_decrypt("ABC", seed_key)

    @pytest.mark.parametrize("ciphertext", [None, 123, b"ABC"])
    def test_rejects_non_string_ciphertext(self, ciphertext):
        with pytest.raises(TypeError, match="text must be a string"):
            autokey_decrypt(ciphertext, "KEY")


class TestAutokeyRoundTrip:
    @pytest.mark.parametrize(
        ("plaintext", "seed_key"),
        [
            ("ATTACK AT DAWN", "QUEEN"),
            ("Mixed CASE, punctuation... 123", "CRYPTO"),
            ("café and Đặng", "KEY"),
            ("A", "LONGERKEY"),
            ("", "A"),
            ("Only punctuation: !? 123", "ABC"),
            ("A-A A A", "BC"),
        ],
    )
    def test_decrypt_after_encrypt_restores_original(self, plaintext, seed_key):
        ciphertext = autokey_encrypt(plaintext, seed_key)
        assert autokey_decrypt(ciphertext, seed_key) == plaintext


class TestAutokeyProgression:
    def test_seed_is_not_repeated(self):
        # Plaintext Autokey: BC is followed by plaintext A, A, A.
        # Repeating-key Vigenere with BC would instead produce BCBCB.
        assert autokey_encrypt("AAAAA", "BC") == "BCAAA"

    def test_punctuation_does_not_consume_keystream(self):
        assert autokey_encrypt("A-A A", "BC") == "B-C A"

    def test_decryption_uses_previously_recovered_plaintext(self):
        # After the seed BC, the keystream continues with plaintext A then B.
        assert autokey_encrypt("ABCD", "BC") == "BDCE"
        assert autokey_decrypt("BDCE", "BC") == "ABCD"
