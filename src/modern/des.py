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


# Expansion E: 32 bits -> 48 bits.
E_TABLE = (
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1,
)


def expand_right_half(right: int) -> int:
    """
    Expand a 32-bit right half into 48 bits using DES E-table.
    """
    return permute(right, E_TABLE, 32)


# DES S-boxes: 8 boxes, each maps 6 bits to 4 bits.
S_BOXES = (
    (
        (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
        (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
        (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
        (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),
    ),
    (
        (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
        (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
        (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
        (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),
    ),
    (
        (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
        (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
        (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
        (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),
    ),
    (
        (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
        (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
        (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
        (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),
    ),
    (
        (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
        (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
        (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
        (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),
    ),
    (
        (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
        (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
        (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
        (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),
    ),
    (
        (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
        (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
        (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
        (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),
    ),
    (
        (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
        (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
        (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
        (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
    ),
)


def substitute(value: int) -> int:
    """
    Apply all eight DES S-boxes to a 48-bit input.

    Returns a 32-bit output.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")

    if not 0 <= value < (1 << 48):
        raise ValueError("value must fit in 48 bits")

    result = 0

    for i in range(8):
        # Extract one 6-bit group, from most significant to least.
        shift = 42 - 6 * i
        block = (value >> shift) & 0b111111

        # Row: first and last bits.
        row = ((block & 0b100000) >> 4) | (block & 0b000001)

        # Column: four middle bits.
        column = (block >> 1) & 0b1111

        # Lookup the corresponding S-box.
        sbox_value = S_BOXES[i][row][column]

        # Append the 4-bit result.
        result = (result << 4) | sbox_value

    return result


# P permutation: 32 bits -> 32 bits.
P_TABLE = (
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25,
)


def permutation_p(value: int) -> int:
    """
    Apply the DES P permutation to a 32-bit value.
    """
    return permute(value, P_TABLE, 32)


def feistel_function(right: int, round_key: int) -> int:
    """
    Apply the DES Feistel function.

    Args:
        right: 32-bit right half.
        round_key: 48-bit round key.

    Returns:
        32-bit Feistel function output.
    """
    if not isinstance(right, int) or isinstance(right, bool):
        raise TypeError("right must be an integer")

    if not isinstance(round_key, int) or isinstance(round_key, bool):
        raise TypeError("round_key must be an integer")

    if not 0 <= right < (1 << 32):
        raise ValueError("right must fit in 32 bits")

    if not 0 <= round_key < (1 << 48):
        raise ValueError("round_key must fit in 48 bits")

    # Step 1: Expand 32 bits to 48 bits.
    expanded = expand_right_half(right)

    # Step 2: XOR with the 48-bit round key.
    mixed = expanded ^ round_key

    # Step 3: Apply the eight S-boxes.
    substituted = substitute(mixed)

    # Step 4: Apply P permutation.
    return permutation_p(substituted)


def encrypt_block(plaintext: int, key: int) -> int:
    """
    Encrypt one 64-bit plaintext block using DES.

    Args:
        plaintext: 64-bit plaintext block.
        key: 64-bit DES key.

    Returns:
        64-bit ciphertext block.
    """
    if not isinstance(plaintext, int) or isinstance(plaintext, bool):
        raise TypeError("plaintext must be an integer")

    if not isinstance(key, int) or isinstance(key, bool):
        raise TypeError("key must be an integer")

    if not 0 <= plaintext < (1 << 64):
        raise ValueError("plaintext must fit in 64 bits")

    if not 0 <= key < (1 << 64):
        raise ValueError("key must fit in 64 bits")

    # Step 1: Generate sixteen round keys.
    round_keys = generate_round_keys(key)

    # Step 2: Apply Initial Permutation.
    permuted = initial_permutation(plaintext)

    # Step 3: Split into two 32-bit halves.
    left = permuted >> 32
    right = permuted & 0xFFFFFFFF

    # Step 4: Perform sixteen Feistel rounds.
    for round_key in round_keys:
        new_left = right
        new_right = left ^ feistel_function(right, round_key)

        left = new_left
        right = new_right

    # Step 5: Swap the two halves.
    combined = (right << 32) | left

    # Step 6: Apply Final Permutation.
    return final_permutation(combined)


def decrypt_block(ciphertext: int, key: int) -> int:
    """
    Decrypt one 64-bit ciphertext block using DES.

    Args:
        ciphertext: 64-bit ciphertext block.
        key: 64-bit DES key.

    Returns:
        64-bit plaintext block.
    """
    if not isinstance(ciphertext, int) or isinstance(ciphertext, bool):
        raise TypeError("ciphertext must be an integer")

    if not isinstance(key, int) or isinstance(key, bool):
        raise TypeError("key must be an integer")

    if not 0 <= ciphertext < (1 << 64):
        raise ValueError("ciphertext must fit in 64 bits")

    if not 0 <= key < (1 << 64):
        raise ValueError("key must fit in 64 bits")

    # Generate round keys and reverse their order.
    round_keys = generate_round_keys(key)[::-1]

    # Apply Initial Permutation.
    permuted = initial_permutation(ciphertext)

    # Split into two 32-bit halves.
    left = permuted >> 32
    right = permuted & 0xFFFFFFFF

    # Perform sixteen Feistel rounds using reversed keys.
    for round_key in round_keys:
        new_left = right
        new_right = left ^ feistel_function(right, round_key)

        left = new_left
        right = new_right

    # Swap the two halves.
    combined = (right << 32) | left

    # Apply Final Permutation.
    return final_permutation(combined)
