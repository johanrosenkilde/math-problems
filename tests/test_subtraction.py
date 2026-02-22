import pytest

from math_problems.subtraction import SubtractionModule, SubtractionProblem, _DIFFICULTY_RANGES


def test_subtraction_problem_result():
    assert SubtractionProblem(7, 3).result == 4
    assert SubtractionProblem(10, 10).result == 0
    assert SubtractionProblem(500, 1).result == 499


def test_generate_returns_nine_problems():
    assert len(SubtractionModule().generate(n=9, difficulty=1)) == 9


def test_generate_custom_count():
    assert len(SubtractionModule().generate(n=5, difficulty=1)) == 5


def test_generate_returns_subtraction_problems():
    for problem in SubtractionModule().generate(n=9, difficulty=1):
        assert isinstance(problem, SubtractionProblem)
        assert isinstance(problem.a, int)
        assert isinstance(problem.b, int)


def test_generate_results_are_non_negative():
    for difficulty in _DIFFICULTY_RANGES:
        for problem in SubtractionModule().generate(n=50, difficulty=difficulty):
            assert problem.result >= 0


@pytest.mark.parametrize("difficulty", _DIFFICULTY_RANGES)
def test_difficulty_range(difficulty):
    low, high = _DIFFICULTY_RANGES[difficulty]
    problems = SubtractionModule().generate(n=50, difficulty=difficulty)
    for p in problems:
        assert low <= p.a <= high
        assert low <= p.b <= p.a


def test_invalid_difficulty():
    with pytest.raises(ValueError):
        SubtractionModule().generate(n=9, difficulty=4)
