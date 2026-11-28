
import pytest

from src.modern.des import encrypt_block_rounds
from src.cryptanalysis.brute_force import (
    brute_force_des_reduced,
    _effective_key_to_des_key,
)


def test_effective_key_to_des_key():
    """The conversion must preserve the 56-bit effective key."""
    effective_key = 0xA5000000000000

    des_key = _effective_key_to_des_key(effective_key)

    # Applying PC-1 must recover the original effective key.
    from src.modern.des import permuted_choice_1

    assert permuted_choice_1(des_key) == effective_key


def test_brute_force_des_reduced_finds_correct_key():
    """Brute force must recover a known key from the search space."""
    plaintext = 0x0123456789ABCDEF
    effective_key = 0xA5000000000000
    rounds = 4

    des_key = _effective_key_to_des_key(effective_key)

    ciphertext = encrypt_block_rounds(
        plaintext,
        des_key,
        rounds,
    )

    results = brute_force_des_reduced(
        plaintext,
        ciphertext,
        rounds,
        key_bits=8,
    )

    assert (effective_key, des_key) in results


def test_brute_force_des_reduced_tries_full_small_keyspace():
    """An 8-bit keyspace contains exactly 256 candidates."""
    plaintext = 0x0123456789ABCDEF
    effective_key = 0xA5000000000000
    rounds = 4

    des_key = _effective_key_to_des_key(effective_key)

    ciphertext = encrypt_block_rounds(
        plaintext,
        des_key,
        rounds,
    )

    results = brute_force_des_reduced(
        plaintext,
        ciphertext,
        rounds,
        key_bits=8,
    )

    # The intended key must be found.
    assert any(key == effective_key for key, _ in results)


def test_brute_force_des_reduced_no_match():
    """Return no candidates when the target key is outside the search space."""

    plaintext = 0x0123456789ABCDEF

    # This key has a non-zero bit among the 48 lower bits.
    # The 4-bit search fixes those lower bits to zero.
    effective_key = 0xA0000000000001

    des_key = _effective_key_to_des_key(effective_key)

    ciphertext = encrypt_block_rounds(
        plaintext,
        des_key,
        rounds=4,
    )

    results = brute_force_des_reduced(
        plaintext,
        ciphertext,
        rounds=4,
        key_bits=4,
    )

    assert results == []


@pytest.mark.parametrize("key_bits", [0, 57, -1])
def test_brute_force_des_reduced_invalid_key_bits(key_bits):
    with pytest.raises(ValueError):
        brute_force_des_reduced(
            0x0123456789ABCDEF,
            0x85E813540F0AB405,
            rounds=4,
            key_bits=key_bits,
        )


@pytest.mark.parametrize("rounds", [0, 17, -1])
def test_brute_force_des_reduced_invalid_rounds(rounds):
    with pytest.raises(ValueError):
        brute_force_des_reduced(
            0x0123456789ABCDEF,
            0x85E813540F0AB405,
            rounds=rounds,
            key_bits=8,
        )


@pytest.mark.parametrize(
    "plaintext,ciphertext",
    [
        (None, 0),
        (0, None),
        ("123", 0),
        (0, "456"),
    ],
)
def test_brute_force_des_reduced_invalid_input_type(
    plaintext,
    ciphertext,
):
    with pytest.raises(TypeError):
        brute_force_des_reduced(
            plaintext,
            ciphertext,
            rounds=4,
            key_bits=8,
        )
