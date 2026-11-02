"""Unit tests for src.mathematics.modular."""

import pytest

from src.mathematics.modular import (
    add_mod,
    extended_gcd,
    gcd,
    is_coprime,
    is_in_zn_star,
    mod_inverse,
    multiply_mod,
    normalize_mod,
    subtract_mod,
    zn_elements,
    zn_star,
)


class TestModularArithmetic:
    @pytest.mark.parametrize(
        ("a", "modulus", "expected"),
        [
            (0, 26, 0),
            (26, 26, 0),
            (27, 26, 1),
            (-1, 26, 25),
            (-27, 26, 25),
            (15, 7, 1),
        ],
    )
    def test_normalize_mod(self, a, modulus, expected):
        assert normalize_mod(a, modulus) == expected

    def test_add_mod(self):
        assert add_mod(20, 10, 26) == 4
        assert add_mod(-2, 5, 26) == 3

    def test_subtract_mod(self):
        assert subtract_mod(5, 10, 26) == 21
        assert subtract_mod(-2, 5, 26) == 19

    def test_multiply_mod(self):
        assert multiply_mod(7, 5, 26) == 9
        assert multiply_mod(-3, 4, 26) == 14

    @pytest.mark.parametrize("function", [normalize_mod, lambda a, m: add_mod(a, 1, m)])
    def test_modular_operation_rejects_non_positive_modulus(self, function):
        with pytest.raises(ValueError):
            function(1, 0)
        with pytest.raises(ValueError):
            function(1, -26)

    def test_modular_operation_rejects_non_integer_values(self):
        with pytest.raises(TypeError):
            normalize_mod(1.5, 26)
        with pytest.raises(TypeError):
            add_mod(True, 1, 26)
        with pytest.raises(TypeError):
            multiply_mod(2, 3, 26.0)


class TestEuclideanAlgorithms:
    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (26, 7, 1),
            (26, 2, 2),
            (-26, 7, 1),
            (0, 26, 26),
            (26, 0, 26),
            (0, 0, 0),
            (-18, -24, 6),
        ],
    )
    def test_gcd(self, a, b, expected):
        assert gcd(a, b) == expected

    @pytest.mark.parametrize(
        ("a", "b"),
        [(26, 7), (26, 2), (-26, 7), (18, -24), (-18, -24), (0, 26), (0, 0)],
    )
    def test_extended_gcd_bezout_identity(self, a, b):
        common_divisor, x, y = extended_gcd(a, b)
        assert common_divisor == gcd(a, b)
        assert a * x + b * y == common_divisor

    def test_extended_gcd_known_example(self):
        common_divisor, x, y = extended_gcd(26, 7)
        assert (common_divisor, x, y) == (1, 3, -11)

    def test_is_coprime(self):
        assert is_coprime(7, 26) is True
        assert is_coprime(2, 26) is False
        assert is_coprime(-7, 26) is True
        assert is_coprime(0, 0) is False

    def test_gcd_rejects_non_integer_values(self):
        with pytest.raises(TypeError):
            gcd(2.5, 5)


class TestModularInverse:
    @pytest.mark.parametrize(
        ("a", "modulus", "expected"),
        [
            (7, 26, 15),
            (3, 26, 9),
            (5, 26, 21),
            (-7, 26, 11),
            (2, 5, 3),
            (1, 2, 1),
        ],
    )
    def test_mod_inverse(self, a, modulus, expected):
        inverse = mod_inverse(a, modulus)
        assert inverse == expected
        assert (a * inverse) % modulus == 1
        assert 0 <= inverse < modulus

    @pytest.mark.parametrize(("a", "modulus"), [(2, 26), (13, 26), (0, 26), (6, 15)])
    def test_mod_inverse_does_not_exist(self, a, modulus):
        with pytest.raises(ValueError, match="no multiplicative inverse"):
            mod_inverse(a, modulus)

    @pytest.mark.parametrize("modulus", [1, 0, -26])
    def test_mod_inverse_requires_modulus_at_least_two(self, modulus):
        with pytest.raises(ValueError):
            mod_inverse(7, modulus)

    def test_mod_inverse_rejects_non_integer_values(self):
        with pytest.raises(TypeError):
            mod_inverse(7.0, 26)
        with pytest.raises(TypeError):
            mod_inverse(7, True)


class TestZnAndZnStar:
    def test_zn_elements_mod_26(self):
        assert zn_elements(26) == list(range(26))

    def test_zn_star_mod_26(self):
        assert zn_star(26) == [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        assert len(zn_star(26)) == 12

    def test_zn_star_for_prime_modulus(self):
        assert zn_star(13) == list(range(1, 13))

    def test_is_in_zn_star(self):
        assert is_in_zn_star(7, 26) is True
        assert is_in_zn_star(2, 26) is False
        assert is_in_zn_star(13, 26) is False
        # 27 represents the same residue class as 1 modulo 26.
        assert is_in_zn_star(27, 26) is True

    @pytest.mark.parametrize("function", [zn_elements, zn_star])
    def test_zn_functions_reject_invalid_modulus(self, function):
        with pytest.raises(ValueError):
            function(1)
        with pytest.raises(ValueError):
            function(0)

    def test_is_in_zn_star_rejects_invalid_arguments(self):
        with pytest.raises(TypeError):
            is_in_zn_star(2.5, 26)
        with pytest.raises(ValueError):
            is_in_zn_star(2, 1)
