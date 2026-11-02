"""Basic number-theory utilities for classical cryptography.

The functions in this module work with any positive modulus; they are not
limited to modulo 26.  For example, the same modular inverse function can be
used by both Affine and Hill ciphers.
"""

from __future__ import annotations


def _require_integer(name: str, value: int) -> None:
    """Raise a clear error unless *value* is an integer (but not a bool)."""
    # bool is a subclass of int in Python, but accepting True as the number 1
    # is usually surprising in mathematical APIs.
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(
            f"{name} must be an integer, got {type(value).__name__}")


def _require_modulus(modulus: int, *, minimum: int = 1) -> None:
    """Validate a modulus.  A modulus must be an integer >= minimum."""
    _require_integer("modulus", modulus)
    if modulus < minimum:
        raise ValueError(f"modulus must be >= {minimum}, got {modulus}")


def normalize_mod(a: int, modulus: int) -> int:
    """Return the canonical residue of *a* in ``0 .. modulus - 1``.

    Python's ``%`` operator already returns a non-negative residue when the
    modulus is positive, including when *a* is negative.
    """
    _require_integer("a", a)
    _require_modulus(modulus)
    return a % modulus


def add_mod(a: int, b: int, modulus: int) -> int:
    """Return ``(a + b) mod modulus`` as a canonical non-negative residue."""
    _require_integer("a", a)
    _require_integer("b", b)
    _require_modulus(modulus)
    return (a + b) % modulus


def subtract_mod(a: int, b: int, modulus: int) -> int:
    """Return ``(a - b) mod modulus`` as a canonical non-negative residue."""
    _require_integer("a", a)
    _require_integer("b", b)
    _require_modulus(modulus)
    return (a - b) % modulus


def multiply_mod(a: int, b: int, modulus: int) -> int:
    """Return ``(a * b) mod modulus`` as a canonical non-negative residue."""
    _require_integer("a", a)
    _require_integer("b", b)
    _require_modulus(modulus)
    return (a * b) % modulus


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of *a* and *b* using Euclid's algorithm.

    The result is always non-negative.  By convention, ``gcd(0, 0) == 0``.
    Negative inputs are supported.
    """
    _require_integer("a", a)
    _require_integer("b", b)

    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return ``(g, x, y)`` such that ``a*x + b*y == g == gcd(a, b)``.

    This is the iterative Extended Euclidean Algorithm.  The GCD is
    non-negative, and signed inputs are supported.
    """
    _require_integer("a", a)
    _require_integer("b", b)

    # Run the algorithm on non-negative values, then restore the signs in the
    # Bézout coefficients so the identity also holds for negative inputs.
    old_r, r = abs(a), abs(b)
    old_x, x = 1, 0
    old_y, y = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

    if a < 0:
        old_x = -old_x
    if b < 0:
        old_y = -old_y

    return old_r, old_x, old_y


def is_coprime(a: int, b: int) -> bool:
    """Return True exactly when *a* and *b* are relatively prime."""
    return gcd(a, b) == 1


def mod_inverse(a: int, modulus: int) -> int:
    """Return the multiplicative inverse of *a* modulo *modulus*.

    The returned value is in ``0 .. modulus - 1``.  An inverse exists exactly
    when ``gcd(a, modulus) == 1``.  Raises ``ValueError`` if the modulus is
    less than 2 or if no inverse exists.
    """
    _require_integer("a", a)
    _require_modulus(modulus, minimum=2)

    common_divisor, x, _ = extended_gcd(a, modulus)
    if common_divisor != 1:
        raise ValueError(
            f"{a} has no multiplicative inverse modulo {modulus}: "
            f"gcd({a}, {modulus}) = {common_divisor}, not 1"
        )

    return x % modulus


def zn_elements(modulus: int) -> list[int]:
    """Return the standard representatives of ``Z_n``: ``[0, ..., n-1]``.

    This project uses moduli of at least 2 for cryptographic operations.
    """
    _require_modulus(modulus, minimum=2)
    return list(range(modulus))


def zn_star(modulus: int) -> list[int]:
    """Return the elements of ``Z_n*`` that have multiplicative inverses.

    In other words, return all ``a`` in ``0 .. modulus - 1`` for which
    ``gcd(a, modulus) == 1``.
    """
    _require_modulus(modulus, minimum=2)
    return [a for a in range(modulus) if gcd(a, modulus) == 1]


def is_in_zn_star(a: int, modulus: int) -> bool:
    """Return whether the residue of *a* belongs to ``Z_n*``.

    Values outside ``0 .. modulus - 1`` are accepted and interpreted by their
    residue class; for example, 27 represents 1 modulo 26.
    """
    _require_integer("a", a)
    _require_modulus(modulus, minimum=2)
    return gcd(a, modulus) == 1
