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
