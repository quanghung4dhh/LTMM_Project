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

from src.mathematics.matrix import (
    determinant,
    matrix_add_mod,
    matrix_inverse_mod,
    matrix_multiply_mod,
    validate_matrix,
)
matrix = [[1, 9, 8],
          [1, 7, 5]]

print(validate_matrix(matrix, square=True))
