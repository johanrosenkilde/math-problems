import pytest

from math_problems.division import (
    DivisionModule,
    DivisionProblem,
    _DIFFICULTY_RANGES,
)


def test_division_problem_dividend():
    assert DivisionProblem(divisor=3, result=4).dividend == 12
    assert DivisionProblem(divisor=7, result=9).dividend == 63
    assert DivisionProblem(divisor=11, result=25).dividend == 275


def test_division_problem_result_is_integer():
    p = DivisionProblem(divisor=6, result=7)
    assert isinstance(p.result, int)
    assert p.dividend % p.divisor == 0


def test_generate_returns_nine_problems():
    assert len(DivisionModule().generate(n=9, difficulty=1)) == 9


def test_generate_custom_count():
    assert len(DivisionModule().generate(n=5, difficulty=1)) == 5


def test_generate_returns_division_problems():
    for problem in DivisionModule().generate(n=9, difficulty=1):
        assert isinstance(problem, DivisionProblem)
        assert isinstance(problem.divisor, int)
        assert isinstance(problem.result, int)


def test_divisor_never_one():
    for difficulty in _DIFFICULTY_RANGES:
        for problem in DivisionModule().generate(n=50, difficulty=difficulty):
            assert problem.divisor != 1


@pytest.mark.parametrize("difficulty", _DIFFICULTY_RANGES)
def test_difficulty_range(difficulty):
    (divisor_low, divisor_high), (result_low, result_high) = _DIFFICULTY_RANGES[difficulty]
    problems = DivisionModule().generate(n=50, difficulty=difficulty)
    for p in problems:
        assert divisor_low <= p.divisor <= divisor_high
        assert result_low <= p.result <= result_high


def test_result_always_integer():
    for difficulty in _DIFFICULTY_RANGES:
        for p in DivisionModule().generate(n=50, difficulty=difficulty):
            assert p.dividend % p.divisor == 0


def test_invalid_difficulty():
    with pytest.raises(ValueError):
        DivisionModule().generate(n=9, difficulty=4)
