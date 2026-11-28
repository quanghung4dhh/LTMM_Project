def permute(value: int, table: tuple[int, ...], input_width: int) -> int:
    """
    Apply a bit permutation using a 1-based DES-style table.

    Bit position 1 refers to the most significant bit.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")

    if not isinstance(table, tuple):
        raise TypeError("table must be a tuple")

    if not isinstance(input_width, int) or isinstance(input_width, bool):
        raise TypeError("input_width must be an integer")

    if input_width <= 0:
        raise ValueError("input_width must be positive")

    if value < 0 or value >= (1 << input_width):
        raise ValueError("value does not fit input_width bits")

    if not table:
        raise ValueError("table must not be empty")

    if any(
        not isinstance(position, int)
        or isinstance(position, bool)
        or position < 1
        or position > input_width
        for position in table
    ):
        raise ValueError("invalid permutation table")

    result = 0

    for position in table:
        bit = (value >> (input_width - position)) & 1
        result = (result << 1) | bit

    return result


# Initial Permutation (IP) table.
# Bit positions are numbered from 1 (MSB) to 64 (LSB).
IP_TABLE = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
)


# Final Permutation (FP) table.
# FP is the inverse permutation of IP.
FP_TABLE = (
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25,
)


def initial_permutation(block: int) -> int:
    """
    Apply the DES Initial Permutation (IP) to a 64-bit block.
    """
    return permute(block, IP_TABLE, 64)


def final_permutation(block: int) -> int:
    """
    Apply the DES Final Permutation (FP) to a 64-bit block.
    """
    return permute(block, FP_TABLE, 64)