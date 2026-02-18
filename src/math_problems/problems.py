import random


def generate_addition_problems(
    n: int = 9, low: int = 1, high: int = 9
) -> list[tuple[int, int]]:
    """Return n random addition problems as (a, b) pairs, a and b in [low, high]."""
    return [(random.randint(low, high), random.randint(low, high)) for _ in range(n)]
