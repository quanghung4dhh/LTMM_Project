from src.classical.vigenere import vigenere_encrypt
from src.cryptanalysis.kasiski import kasiski_examination


def test_kasiski_detects_known_vigenere_key_length():
    # Arrange: create plaintext with repeated patterns.
    plaintext = "THEXYTHEXYTHE"
    key = "LEMON"

    # Encrypt plaintext using Vigenere.
    ciphertext = vigenere_encrypt(plaintext, key)

    # Act: perform Kasiski examination.
    result = kasiski_examination(
        ciphertext,
        n=3,
        min_key_length=2,
        max_key_length=20,
    )

    # Assert: the actual key length should be detected.
    assert len(key) in [
        key_length
        for key_length, score in result["candidates"]
    ]

    # The controlled example should rank key length 5 first.
    assert result["candidates"][0] == (5, 5)
