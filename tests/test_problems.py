import pytest

from math_problems.problems import _DIFFICULTY_RANGES, generate_addition_problems


def test_returns_nine_problems():
    assert len(generate_addition_problems()) == 9


def test_custom_count():
    assert len(generate_addition_problems(n=5)) == 5


def test_returns_tuples_of_ints():
    for problem in generate_addition_problems():
        assert isinstance(problem, tuple)
        assert len(problem) == 2
        assert all(isinstance(v, int) for v in problem)


@pytest.mark.parametrize("difficulty", _DIFFICULTY_RANGES)
def test_difficulty_range(difficulty):
    low, high = _DIFFICULTY_RANGES[difficulty]
    problems = generate_addition_problems(n=50, difficulty=difficulty)
    for a, b in problems:
        assert low <= a <= high
        assert low <= b <= high


def test_invalid_difficulty():
    with pytest.raises(ValueError):
        generate_addition_problems(difficulty=4)
