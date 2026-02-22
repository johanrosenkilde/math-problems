import pytest

from math_problems.multiplication import (
    MultiplicationModule,
    MultiplicationProblem,
    _DIFFICULTY_RANGES,
)


def test_multiplication_problem_result():
    assert MultiplicationProblem(3, 4).result == 12
    assert MultiplicationProblem(1, 1).result == 1
    assert MultiplicationProblem(11, 25).result == 275


def test_generate_returns_nine_problems():
    assert len(MultiplicationModule().generate(n=9, difficulty=1)) == 9


def test_generate_custom_count():
    assert len(MultiplicationModule().generate(n=5, difficulty=1)) == 5


def test_generate_returns_multiplication_problems():
    for problem in MultiplicationModule().generate(n=9, difficulty=1):
        assert isinstance(problem, MultiplicationProblem)
        assert isinstance(problem.a, int)
        assert isinstance(problem.b, int)


@pytest.mark.parametrize("difficulty", _DIFFICULTY_RANGES)
def test_difficulty_range(difficulty):
    (a_low, a_high), (b_low, b_high) = _DIFFICULTY_RANGES[difficulty]
    problems = MultiplicationModule().generate(n=50, difficulty=difficulty)
    for p in problems:
        assert a_low <= p.a <= a_high
        assert b_low <= p.b <= b_high


def test_invalid_difficulty():
    with pytest.raises(ValueError):
        MultiplicationModule().generate(n=9, difficulty=4)
