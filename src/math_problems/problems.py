import random

_DIFFICULTY_RANGES: dict[int, tuple[int, int]] = {
    1: (1, 9),
    2: (10, 99),
    3: (100, 499),
}


def generate_addition_problems(
    n: int = 9, difficulty: int = 1
) -> list[tuple[int, int]]:
    """Return n random addition problems as (a, b) pairs for the given difficulty.

    Valid difficulty levels and their addend ranges are defined in _DIFFICULTY_RANGES.
    """
    if difficulty not in _DIFFICULTY_RANGES:
        raise ValueError(f"Difficulty must be 1, 2, or 3, got {difficulty}.")
    low, high = _DIFFICULTY_RANGES[difficulty]
    return [(random.randint(low, high), random.randint(low, high)) for _ in range(n)]
