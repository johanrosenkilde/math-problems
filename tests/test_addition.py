import pytest

from math_problems.addition import AdditionModule, AdditionProblem, _DIFFICULTY_RANGES


def test_addition_problem_result():
    assert AdditionProblem(3, 4).result == 7
    assert AdditionProblem(0, 0).result == 0
    assert AdditionProblem(100, 200).result == 300


def test_generate_returns_nine_problems():
    assert len(AdditionModule().generate(n=9, difficulty=1)) == 9


def test_generate_custom_count():
    assert len(AdditionModule().generate(n=5, difficulty=1)) == 5


def test_generate_returns_addition_problems():
    for problem in AdditionModule().generate(n=9, difficulty=1):
        assert isinstance(problem, AdditionProblem)
        assert isinstance(problem.a, int)
        assert isinstance(problem.b, int)


@pytest.mark.parametrize("difficulty", _DIFFICULTY_RANGES)
def test_difficulty_range(difficulty):
    low, high = _DIFFICULTY_RANGES[difficulty]
    problems = AdditionModule().generate(n=50, difficulty=difficulty)
    for p in problems:
        assert low <= p.a <= high
        assert low <= p.b <= high


def test_invalid_difficulty():
    with pytest.raises(ValueError):
        AdditionModule().generate(n=9, difficulty=4)
