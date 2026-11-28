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

# Permuted Choice 1 (PC-1): 64 bits -> 56 bits.
PC1_TABLE = (
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4,
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


def permuted_choice_1(key: int) -> int:
    """
    Apply PC-1 to a 64-bit DES key.

    Returns a 56-bit effective key.
    """
    return permute(key, PC1_TABLE, 64)


def split_key(key_56: int) -> tuple[int, int]:
    """
    Split a 56-bit effective key into two 28-bit halves.
    """
    if not isinstance(key_56, int) or isinstance(key_56, bool):
        raise TypeError("key_56 must be an integer")

    if not 0 <= key_56 < (1 << 56):
        raise ValueError("key_56 must fit in 56 bits")

    c = key_56 >> 28
    d = key_56 & ((1 << 28) - 1)

    return c, d


# Number of left circular shifts for each DES round.
SHIFT_SCHEDULE = (
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1,
)


def left_circular_shift(value: int, shift: int, width: int = 28) -> int:
    """
    Perform a left circular shift on a fixed-width integer.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")

    if not isinstance(width, int) or isinstance(width, bool):
        raise TypeError("width must be an integer")

    if not isinstance(shift, int) or isinstance(shift, bool):
        raise TypeError("shift must be an integer")

    if width <= 0:
        raise ValueError("width must be positive")

    if not 0 <= value < (1 << width):
        raise ValueError("value does not fit specified width")

    if not 0 <= shift <= width:
        raise ValueError("invalid shift amount")

    mask = (1 << width) - 1

    return ((value << shift) | (value >> (width - shift))) & mask


# Permuted Choice 2 (PC-2): 56 bits -> 48 bits.
PC2_TABLE = (
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32,
)


def permuted_choice_2(key_56: int) -> int:
    """
    Apply PC-2 to a 56-bit combined key.

    Returns a 48-bit round key.
    """
    return permute(key_56, PC2_TABLE, 56)


def generate_round_keys(key: int) -> tuple[int, ...]:
    """
    Generate sixteen 48-bit DES round keys from a 64-bit key.
    """
    if not isinstance(key, int) or isinstance(key, bool):
        raise TypeError("key must be an integer")

    if not 0 <= key < (1 << 64):
        raise ValueError("key must fit in 64 bits")

    # Step 1: Apply PC-1.
    effective_key = permuted_choice_1(key)

    # Step 2: Split into two 28-bit halves.
    c, d = split_key(effective_key)

    round_keys = []

    # Step 3: Generate sixteen round keys.
    for shift in SHIFT_SCHEDULE:

        # Circular left shifts.
        c = left_circular_shift(c, shift, 28)
        d = left_circular_shift(d, shift, 28)

        # Combine C and D into a 56-bit value.
        combined = (c << 28) | d

        # Apply PC-2 to obtain a 48-bit round key.
        round_key = permuted_choice_2(combined)

        round_keys.append(round_key)

    return tuple(round_keys)
