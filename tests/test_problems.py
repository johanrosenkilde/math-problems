import pytest

from math_problems.problems import generate_addition_problems


def test_returns_nine_problems():
    assert len(generate_addition_problems()) == 9


def test_custom_count():
    assert len(generate_addition_problems(n=5)) == 5


def test_returns_tuples_of_ints():
    for problem in generate_addition_problems():
        assert isinstance(problem, tuple)
        assert len(problem) == 2
        assert all(isinstance(v, int) for v in problem)


def test_difficulty_1_range():
    problems = generate_addition_problems(n=50, difficulty=1)
    for a, b in problems:
        assert 1 <= a <= 9
        assert 1 <= b <= 9


def test_difficulty_2_range():
    problems = generate_addition_problems(n=50, difficulty=2)
    for a, b in problems:
        assert 10 <= a <= 50
        assert 10 <= b <= 50


def test_difficulty_3_range():
    problems = generate_addition_problems(n=50, difficulty=3)
    for a, b in problems:
        assert 50 <= a <= 250
        assert 50 <= b <= 250


def test_invalid_difficulty():
    with pytest.raises(ValueError):
        generate_addition_problems(difficulty=4)
