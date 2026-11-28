import pytest

from src.modern.des import (
    permute,
    initial_permutation,
    final_permutation,
    permuted_choice_1,
    split_key,
    left_circular_shift,
    permuted_choice_2,
    generate_round_keys,
)


def test_permute_identity():
    value = 0b10110010
    table = (1, 2, 3, 4, 5, 6, 7, 8)

    assert permute(value, table, 8) == value


def test_permute_reverse():
    value = 0b10110010
    table = (8, 7, 6, 5, 4, 3, 2, 1)

    assert permute(value, table, 8) == 0b01001101


def test_permute_invalid_value():
    with pytest.raises(ValueError):
        permute(256, (1, 2, 3), 8)


def test_permute_invalid_table():
    with pytest.raises(ValueError):
        permute(0b10110010, (1, 2, 9), 8)


def test_permute_empty_table():
    with pytest.raises(ValueError):
        permute(0b10110010, (), 8)


def test_initial_permutation_known_vector():
    plaintext = 0x0123456789ABCDEF

    expected = 0xCC00CCFFF0AAF0AA

    assert initial_permutation(plaintext) == expected


def test_final_permutation_known_vector():
    value = 0xCC00CCFFF0AAF0AA

    expected = 0x0123456789ABCDEF

    assert final_permutation(value) == expected


def test_ip_and_fp_are_inverse():
    plaintext = 0x0123456789ABCDEF

    result = final_permutation(
        initial_permutation(plaintext)
    )

    assert result == plaintext


def test_fp_and_ip_are_inverse():
    block = 0xFEDCBA9876543210

    result = initial_permutation(
        final_permutation(block)
    )

    assert result == block


def test_permuted_choice_1_known_vector():
    key = 0x133457799BBCDFF1

    assert permuted_choice_1(key) == 0xF0CCAAF556678F


def test_split_key():
    key_56 = 0xF0CCAAF556678F

    c, d = split_key(key_56)

    assert c == 0xF0CCAAF
    assert d == 0x556678F


def test_left_circular_shift():
    value = 0b10110010

    result = left_circular_shift(value, 1, 8)

    assert result == 0b01100101


def test_permuted_choice_2_known_vector():
    key_56 = 0xE19955FAACCF1E

    assert permuted_choice_2(key_56) == 0x1B02EFFC7072


def test_generate_round_keys_count():
    key = 0x133457799BBCDFF1

    round_keys = generate_round_keys(key)

    assert len(round_keys) == 16


def test_generate_round_keys_width():
    key = 0x133457799BBCDFF1

    round_keys = generate_round_keys(key)

    assert all(0 <= round_key < (1 << 48) for round_key in round_keys)


def test_generate_round_keys_known_vectors():
    key = 0x133457799BBCDFF1

    round_keys = generate_round_keys(key)

    assert round_keys[0] == 0x1B02EFFC7072
    assert round_keys[-1] == 0xCB3D8B0E17F5


def test_generate_round_keys_invalid_key():
    with pytest.raises(ValueError):
        generate_round_keys(1 << 64)
