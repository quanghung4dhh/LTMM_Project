import pytest

from src.modern.des import (
    permute,
    initial_permutation,
    final_permutation,
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
