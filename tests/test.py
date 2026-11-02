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

# a = normalize_mod(-1002, 25)
# print(a)

# a = gcd(3,99)
# print(a)

a = mod_inverse(3, 21)
print(a)