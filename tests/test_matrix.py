"""Unit tests for src.mathematics.matrix."""

import pytest

from src.mathematics.matrix import (
    determinant,
    matrix_add_mod,
    matrix_inverse_mod,
    matrix_multiply_mod,
    validate_matrix,
)


class TestValidateMatrix:
    def test_validate_matrix_returns_shape(self):
        assert validate_matrix([[1, 2, 3], [4, 5, 6]]) == (2, 3)
        assert validate_matrix([[1, 2], [3, 4]], square=True) == (2, 2)

    @pytest.mark.parametrize("invalid_matrix", [[], [[], []]])
    def test_rejects_empty_matrix_or_empty_rows(self, invalid_matrix):
        with pytest.raises(ValueError):
            validate_matrix(invalid_matrix)

    def test_rejects_ragged_matrix(self):
        with pytest.raises(ValueError, match="rectangular"):
            validate_matrix([[1, 2], [3]])

    def test_rejects_non_square_matrix_when_required(self):
        with pytest.raises(ValueError, match="square"):
            validate_matrix([[1, 2, 3], [4, 5, 6]], square=True)

    @pytest.mark.parametrize("invalid_matrix", ["123", b"123", None, 42])
    def test_rejects_invalid_matrix_container(self, invalid_matrix):
        with pytest.raises(TypeError):
            validate_matrix(invalid_matrix)

    def test_rejects_non_sequence_row(self):
        with pytest.raises(TypeError, match="row 0"):
            validate_matrix([1, 2, 3])

    @pytest.mark.parametrize("invalid_value", [1.5, "2", True, None])
    def test_rejects_non_integer_matrix_entries(self, invalid_value):
        with pytest.raises(TypeError, match=r"matrix\[0\]\[1\]"):
            validate_matrix([[1, invalid_value]])


class TestMatrixAddition:
    def test_add_mod_2x2(self):
        left = [[1, 2], [3, 4]]
        right = [[5, 6], [7, 8]]
        assert matrix_add_mod(left, right, 26) == [[6, 8], [10, 12]]

    def test_add_mod_normalizes_negative_and_large_values(self):
        left = [[-1, 30], [27, -28]]
        right = [[2, 1], [-2, 3]]
        assert matrix_add_mod(left, right, 26) == [[1, 5], [25, 1]]

    def test_add_mod_supports_rectangular_matrices(self):
        assert matrix_add_mod([[1, 2, 3]], [[4, 5, 6]], 10) == [[5, 7, 9]]

    def test_add_mod_rejects_different_shapes(self):
        with pytest.raises(ValueError, match="same dimensions"):
            matrix_add_mod([[1, 2]], [[1], [2]], 26)

    @pytest.mark.parametrize("modulus", [0, 1, -26])
    def test_add_mod_rejects_invalid_modulus(self, modulus):
        with pytest.raises(ValueError):
            matrix_add_mod([[1]], [[2]], modulus)

    def test_add_mod_rejects_non_integer_modulus(self):
        with pytest.raises(TypeError):
            matrix_add_mod([[1]], [[2]], 26.0)


class TestMatrixMultiplication:
    def test_multiply_mod_2x2(self):
        left = [[1, 2], [3, 4]]
        right = [[5, 6], [7, 8]]
        assert matrix_multiply_mod(left, right, 26) == [[19, 22], [17, 24]]

    def test_multiply_mod_rectangular_matrices(self):
        # A (2x3) matrix multiplied by a (3x2) matrix gives a (2x2) matrix.
        left = [[1, 2, 3], [4, 5, 6]]
        right = [[7, 8], [9, 10], [11, 12]]
        assert matrix_multiply_mod(left, right, 100) == [
            [58, 64], [139 % 100, 154 % 100]]

    def test_multiply_mod_normalizes_negative_values(self):
        assert matrix_multiply_mod([[-1, 2]], [[3], [4]], 26) == [[5]]

    def test_multiply_mod_rejects_incompatible_dimensions(self):
        with pytest.raises(ValueError, match="incompatible"):
            matrix_multiply_mod([[1, 2]], [[1, 2]], 26)

    def test_multiply_mod_rejects_invalid_modulus(self):
        with pytest.raises(ValueError):
            matrix_multiply_mod([[1]], [[1]], 1)


class TestDeterminant:
    @pytest.mark.parametrize(
        ("matrix", "expected"),
        [
            ([[7]], 7),
            ([[1, 2], [3, 4]], -2),
            ([[3, 3], [2, 5]], 9),
            ([[1, 2], [2, 4]], 0),
            ([[0, 1], [1, 0]], -1),  # Requires a row swap.
            ([[1, 2, 3], [0, 1, 4], [5, 6, 0]], 1),
            ([[2, 0, 1], [3, 0, 0], [5, 1, 1]], 3),
            ([[-1, 2], [3, 4]], -10),
        ],
    )
    def test_determinant(self, matrix, expected):
        # Determinants are exact integers; they are not reduced modulo 26.
        assert determinant(matrix) == expected

    def test_determinant_rejects_non_square_matrix(self):
        with pytest.raises(ValueError, match="square"):
            determinant([[1, 2, 3], [4, 5, 6]])


class TestMatrixInverse:
    def test_inverse_mod_2x2(self):
        matrix = [[3, 3], [2, 5]]
        expected_inverse = [[15, 17], [20, 9]]
        inverse = matrix_inverse_mod(matrix, 26)

        assert inverse == expected_inverse
        assert matrix_multiply_mod(matrix, inverse, 26) == [[1, 0], [0, 1]]
        assert matrix_multiply_mod(inverse, matrix, 26) == [[1, 0], [0, 1]]

    def test_inverse_mod_3x3(self):
        matrix = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
        inverse = matrix_inverse_mod(matrix, 26)
        identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        assert matrix_multiply_mod(matrix, inverse, 26) == identity
        assert matrix_multiply_mod(inverse, matrix, 26) == identity

    def test_inverse_mod_1x1(self):
        assert matrix_inverse_mod([[7]], 26) == [[15]]

    def test_inverse_mod_supports_row_swap_case(self):
        matrix = [[0, 1], [1, 0]]
        assert matrix_inverse_mod(matrix, 26) == [[0, 1], [1, 0]]

    def test_inverse_mod_normalizes_negative_entries(self):
        matrix = [[-1, 0], [0, 1]]
        inverse = matrix_inverse_mod(matrix, 26)
        assert matrix_multiply_mod(matrix, inverse, 26) == [[1, 0], [0, 1]]

    @pytest.mark.parametrize(
        "matrix",
        [
            [[2, 0], [0, 1]],  # determinant 2 is not invertible modulo 26.
            [[13, 0], [0, 1]],  # determinant 13 is not invertible modulo 26.
            [[1, 2], [2, 4]],  # determinant is zero.
        ],
    )
    def test_inverse_mod_rejects_non_invertible_matrices(self, matrix):
        with pytest.raises(ValueError, match="no inverse"):
            matrix_inverse_mod(matrix, 26)

    def test_inverse_mod_rejects_non_square_matrix(self):
        with pytest.raises(ValueError, match="square"):
            matrix_inverse_mod([[1, 2, 3], [4, 5, 6]], 26)

    @pytest.mark.parametrize("modulus", [0, 1, -26])
    def test_inverse_mod_rejects_invalid_modulus(self, modulus):
        with pytest.raises(ValueError):
            matrix_inverse_mod([[1, 0], [0, 1]], modulus)

    def test_inverse_mod_rejects_non_integer_modulus(self):
        with pytest.raises(TypeError):
            matrix_inverse_mod([[1]], 26.0)


class TestInputValidation:
    def test_matrix_operation_rejects_invalid_matrix_entry(self):
        with pytest.raises(TypeError):
            matrix_add_mod([[1, 2.5]], [[1, 2]], 26)

    def test_matrix_multiplication_does_not_mutate_inputs(self):
        left = [[1, 2], [3, 4]]
        right = [[5, 6], [7, 8]]
        left_before = [row[:] for row in left]
        right_before = [row[:] for row in right]

        matrix_multiply_mod(left, right, 26)

        assert left == left_before
        assert right == right_before

    def test_matrix_inverse_does_not_mutate_input(self):
        matrix = [[3, 3], [2, 5]]
        original = [row[:] for row in matrix]

        matrix_inverse_mod(matrix, 26)

        assert matrix == original
