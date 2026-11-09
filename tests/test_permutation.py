
"""Unit tests for permutation utilities."""

import pytest

from src.mathematics.permutation import validate_permutation


class TestValidatePermutation:

    @pytest.mark.parametrize(
        "permutation",
        [
            [3, 1, 4, 2],
            [1, 2, 3, 4],
            [4, 3, 2, 1],
            [1],
            (3, 1, 2),
            range(1, 5),
        ],
    )
    def test_accepts_valid_permutations(self, permutation):
        assert validate_permutation(permutation) > 0

    @pytest.mark.parametrize(
        "permutation",
        [
            [1, 1, 3],
            [2, 2],
            [1, 2, 2, 4],
        ],
    )
    def test_rejects_duplicate_values(self, permutation):
        with pytest.raises(ValueError, match="duplicate"):
            validate_permutation(permutation)

    @pytest.mark.parametrize(
        "permutation",
        [
            [0, 2, 3],
            [-1, 2, 3],
            [1, 2, 4],
            [1, 2, 3, 5],
        ],
    )
    def test_rejects_values_outside_valid_range(self, permutation):
        with pytest.raises(ValueError):
            validate_permutation(permutation)

    def test_rejects_empty_permutation(self):
        with pytest.raises(ValueError):
            validate_permutation([])

    @pytest.mark.parametrize(
        "permutation",
        [
            None,
            123,
            "123",
            b"123",
            {1, 2, 3},
        ],
    )
    def test_rejects_invalid_containers(self, permutation):
        with pytest.raises(TypeError):
            validate_permutation(permutation)

    @pytest.mark.parametrize(
        "permutation",
        [
            [True, 2, 3],
            [1, False, 3],
            [1, 2.5, 3],
            [1, "2", 3],
            [1, None, 3],
        ],
    )
    def test_rejects_non_integer_elements(self, permutation):
        with pytest.raises(TypeError):
            validate_permutation(permutation)
