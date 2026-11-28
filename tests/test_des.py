import pytest

from src.modern.des import permute


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
